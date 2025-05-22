from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_drugs_drogaraia(search_term, cep, drugstore_base_url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    wait = WebDriverWait(driver, 15)
    driver.get(f'{drugstore_base_url}search?w={search_term}&viewport=&limit=24&p=1&sort=relevance%3Adesc')
    driver.maximize_window()
    time.sleep(2)
    drugs = []

    try:
        accept_cookies_btn = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        wait.until(EC.element_to_be_clickable(accept_cookies_btn))
        accept_cookies_btn.click()
    except Exception as e:
        print(f'Error cookie: {e}')

    try:
        cep_btn = driver.find_element(By.XPATH, '//*[@id="menuContainer"]/div/div[1]/div[1]/button')
        wait.until(EC.element_to_be_clickable(cep_btn))              
        cep_btn.click()
    except Exception as e:
        print(f'Error cep 1: {e}')

    try:
        cep_input = driver.find_element(By.XPATH, '//input[@id="cep"]')
        wait.until(EC.visibility_of(cep_input))
        cep_input.clear()
        cep_input.send_keys(cep)
    except Exception as e:
        print(f'Error cep 2: {e}')

    try:
        continue_btn = driver.find_element(By.XPATH, '//*[@id="side-sheet-desktop"]/div/div[3]/div[2]/button')
        wait.until(EC.element_to_be_clickable(continue_btn))
        continue_btn.click()
    except Exception as e:
        print(f'Error cep 3: {e}')

    drugs_el = driver.find_elements(By.XPATH, '//div[@data-testid="container-products"]/article')
    
    for drug in drugs_el:          
        try:
            sponsored_tag = drug.find_element(By.XPATH, './/div[@data-testid="sponsored-tag"]') if True else False
        except Exception as e:
            sponsored_tag = False

        if (sponsored_tag == False):
            try:
                id = drug.get_attribute('data-item-id')
            except:
                id = ''
                print(f'Error (id {id}) id: {e}')

            try:
                description_el = drug.find_element(By.XPATH, './/h2/a')
                description = description_el.text
                link = description_el.get_attribute('href')
            except Exception as e:
                description = ''
                link = ''
                print(f'Error (id {id}) description or link: {e}')

            try:
                short_description = drug.find_element(By.XPATH, './/h2/following-sibling::div[1]/a').text
            except Exception as e:
                short_description = ''
                print(f'Error (id {id}) short_description: {e}')

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
                print(f'Error (id {id}) price: {e}')

            try:
                quantity = drug.find_element(By.XPATH, './/div/p').text
            except Exception as e:
                quantity = ''
                print(f'Error (id {id}) quantity: {e}')

            drugs.append({
                'id': id,
                'description': description,
                'link': link,
                'short_description': short_description,
                'quantity': quantity,
                'price': price,
                'price_str': price_str,
                'drugstore': drugstore_base_url.split('.')[1].upper()
            })

    driver.quit()
    return drugs

def search_drugs_pacheco(search_term, cep, drugstore_base_url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    wait = WebDriverWait(driver, 15)
    driver.get(f'https://www.drogariaspacheco.com.br/pesquisa?q={search_term}')
    driver.maximize_window()
    time.sleep(2)
    drugs = []

    try:
        accept_cookies_btn = driver.find_element(By.XPATH, '//*[@id="dm876A"]/div')
        wait.until(EC.element_to_be_clickable(accept_cookies_btn))
        accept_cookies_btn.click()
    except Exception as e:
        print(f'Error cookie: {e}')

    drugs_el = driver.find_elements(By.XPATH, '//*[@id="inicio-conteudo"]/div[5]/div/div[1]/div/div[1]/ul')
    
    for drug in drugs_el:          
        # NÃO MODIFIQUEI DAQUI PARA BAIXO
        try:
            id = drug.find_element(By.XPATH, './/h2/a')
        except:
            id = ''
            print(f'Error (id {id}) id: {e}')

        try:
            description_el = drug.find_element(By.XPATH, './/h2/a')
            description = description_el.text
            link = description_el.get_attribute('href')
        except Exception as e:
            description = ''
            link = ''
            print(f'Error (id {id}) description or link: {e}')

        try:
            short_description = drug.find_element(By.XPATH, './/h2/following-sibling::div[1]/a').text
        except Exception as e:
            short_description = ''
            print(f'Error (id {id}) short_description: {e}')

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
            print(f'Error (id {id}) price: {e}')

        try:
            quantity = drug.find_element(By.XPATH, './/div/p').text
        except Exception as e:
            quantity = ''
            print(f'Error (id {id}) quantity: {e}')

        drugs.append({
            'id': id,
            'description': description,
            'link': link,
            'short_description': short_description,
            'quantity': quantity,
            'price': price,
            'price_str': price_str,
            'drugstore': drugstore_base_url.split('.')[1].upper()
        })

    driver.quit()
    return drugs