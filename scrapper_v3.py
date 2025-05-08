from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def search_drugs(searchTerm, cep, limit):
    drugs = []
    loadTime = 1
    productsPerPage = 48
    url = f'https://www.drogaraia.com.br/search?w={searchTerm}&viewport=&limit={productsPerPage}&p=1'

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(loadTime)

    try:
        acceptCookiesButton = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        time.sleep(loadTime)

        acceptCookiesButton.click()
        time.sleep(loadTime)
    except Exception as e:
        print(f'Error cookie: {e}')

    try:
        cepButton = driver.find_element(By.XPATH, '//*[@id="menuContainer"]/div/div[1]/div[1]/button')
        time.sleep(loadTime)
                
        cepButton.click()
        time.sleep(loadTime)

        cepInput = driver.find_element(By.XPATH, '//input[@id="cep"]')
        time.sleep(loadTime)

        cepInput.clear()
        cepInput.send_keys(cep)
        time.sleep(loadTime)

        continueButton = driver.find_element(By.XPATH, '//*[@id="side-sheet-desktop"]/div/div[3]/div[2]/button')
        time.sleep(loadTime)

        continueButton.click()
        time.sleep(loadTime)
    except Exception as e:
        print(f'Error cep: {e}')

    pages = int(driver.find_element(By.XPATH, '//*[@id="__next"]/main/main/div/div/section/section/div[1]/div[2]/nav/ol/li[3]/a/button').text) or 1

    for page in range(1, pages + 1):
        url = f'https://www.drogaraia.com.br/search?w={searchTerm}&viewport=&limit={productsPerPage}&p={page}'

        drugsEl = driver.find_elements(By.XPATH, '//div[@data-testid="container-products"]/article')
        time.sleep(loadTime)
        
        for i, drug in enumerate(drugsEl):
            if (limit and i > int(limit)):
                break
            
            try:
                sponsoredTag = drug.find_element(By.XPATH, './/div[@data-testid="sponsored-tag"]') if True else False
            except Exception as e:
                sponsoredTag = False

            if (sponsoredTag == False):
                try:
                    id = drug.get_attribute('data-item-id')
                    priceType = drug.get_attribute('data-price-type').upper()
                except:
                    id = ''
                    print(f'Error (page {page}, id {id}) id: {e}')

                try:
                    descriptionEl = drug.find_element(By.XPATH, './/h2/a')
                    description = descriptionEl.text
                    link = descriptionEl.get_attribute('href')
                except Exception as e:
                    description = ''
                    link = ''
                    print(f'Error (page {page}, id {id}) description or link: {e}')

                try:
                    shortDescription = drug.find_element(By.XPATH, './/h2/following-sibling::div[1]/a').text
                except Exception as e:
                    shortDescription = ''
                    print(f'Error (page {page}, id {id}) shortDescription: {e}')

                try:
                    discountedPrice = drug.find_elements(By.XPATH, './/div[@data-testid="price"]')
                    if (len(discountedPrice) > 1):
                        price = discountedPrice[1].text
                    elif (len(discountedPrice) == 1):
                        price = discountedPrice[0].text
                    else:
                        try:
                            price = drug.find_element(By.XPATH, './/div[@class="sc-893b29e9-0 hUuLwk"]/div').text 
                        except:
                            price = drug.find_element(By.XPATH, './div[2]/div[3]/div/div/div/text()').text
                    price = float(price.replace("R$", "").strip().replace(",", "."))
                except Exception as e:
                    price = ''
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
                    'short_description': shortDescription,
                    'quantity': quantity,
                    'price': price,
                    'drugstore': 'DROGA RAIA'
                })
            
        if page > 1:
            driver.get(url)
            time.sleep(loadTime)

    driver.close()

    return {
        'count': len(drugs),
        'drugs': drugs
    }