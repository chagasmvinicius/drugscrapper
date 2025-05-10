from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def search_drugs(search_term, cep, drugstore_base_url):
    drugstore_name = drugstore_base_url.split('.')[1].upper()
    drugs = []
    load_time = 1
    products_per_page = 48
    url = f'{drugstore_base_url}search?w={search_term}&viewport=&limit={products_per_page}&p=1'

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(load_time)

    try:
        accept_cookies_btn = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        time.sleep(load_time)

        accept_cookies_btn.click()
        time.sleep(load_time)
    except Exception as e:
        print(f'Error cookie: {e}')

    try:
        cep_btn = driver.find_element(By.XPATH, '//*[@id="menuContainer"]/div/div[1]/div[1]/button')
        time.sleep(load_time)
                
        cep_btn.click()
        time.sleep(load_time)

        cep_input = driver.find_element(By.XPATH, '//input[@id="cep"]')
        time.sleep(load_time)

        cep_input.clear()
        cep_input.send_keys(cep)
        time.sleep(load_time)

        continue_btn = driver.find_element(By.XPATH, '//*[@id="side-sheet-desktop"]/div/div[3]/div[2]/button')
        time.sleep(load_time)

        continue_btn.click()
        time.sleep(load_time)
    except Exception as e:
        print(f'Error cep: {e}')

    pages = int(driver.find_element(By.XPATH, '//*[@id="__next"]/main/main/div/div/section/section/div[1]/div[2]/nav/ol/li[3]/a/button').text) or 1

    for page in range(1, pages + 1):
        url = f'{drugstore_base_url}search?w={search_term}&viewport=&limit={products_per_page}&p={page}'

        drugs_el = driver.find_elements(By.XPATH, '//div[@data-testid="container-products"]/article')
        time.sleep(load_time)
        
        for i, drug in enumerate(drugs_el):          
            try:
                sponsored_tag = drug.find_element(By.XPATH, './/div[@data-testid="sponsored-tag"]') if True else False
            except Exception as e:
                sponsored_tag = False

            if (sponsored_tag == False):
                try:
                    id = drug.get_attribute('data-item-id')
                    price_type = drug.get_attribute('data-price-type').upper()
                except:
                    id = ''
                    print(f'Error (page {page}, id {id}) id: {e}')

                try:
                    description_el = drug.find_element(By.XPATH, './/h2/a')
                    description = description_el.text
                    link = description_el.get_attribute('href')
                except Exception as e:
                    description = ''
                    link = ''
                    print(f'Error (page {page}, id {id}) description or link: {e}')

                try:
                    short_description = drug.find_element(By.XPATH, './/h2/following-sibling::div[1]/a').text
                except Exception as e:
                    short_description = ''
                    print(f'Error (page {page}, id {id}) short_description: {e}')

                try:
                    discounted_price = drug.find_elements(By.XPATH, './/div[@data-testid="price"]')
                    if (len(discounted_price) > 1):
                        price = discounted_price[1].text
                    elif (len(discounted_price) == 1):
                        price = discounted_price[0].text
                    else:
                        try:
                            price = drug.find_element(By.XPATH, './/div[@class="sc-893b29e9-0 hUuLwk"]/div').text 
                        except:
                            price = drug.find_element(By.XPATH, './div[2]/div[3]/div/div/div/text()').text
                    price_str = price
                    price = float(price.replace("R$", "").strip().replace(",", ".")) or 0.0
                except Exception as e:
                    price = 0.0
                    price_str = ''
                    print(f'Error (page {page}, id {id}) price: {e}')

                try:
                    quantity = drug.find_element(By.XPATH, './/div/p').text
                except Exception as e:
                    quantity = ''
                    print(f'Error (page {page}, id {id}) quantity: {e}')

                drugs.append({
                    'id': id,
                    'description': description,
                    'link': link,
                    'short_description': short_description,
                    'quantity': quantity,
                    'price': price,
                    'price_str': price_str,
                    'drugstore': drugstore_name
                })
            
        if page > 1:
            driver.get(url)
            time.sleep(load_time)

    driver.close()
    return drugs