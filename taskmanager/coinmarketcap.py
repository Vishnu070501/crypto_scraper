import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class CoinMarketCap:
    def __init__(self, coin):
        self.coin = coin
        self.url = f"https://coinmarketcap.com/currencies/{coin.lower()}"
        print(coin)

    def scrape_data(self):
        # Set the path to your ChromeDriver executable
        service = Service('/usr/local/bin/chromedriver-linux64/chromedriver')  # Adjust this path to your actual ChromeDriver path
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Explicitly specify the path to the Google Chrome binary
        options.binary_location = '/usr/bin/google-chrome'  # Adjust this path if necessary

        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(self.url)
            wait = WebDriverWait(driver, 20)

            # Scrape the required data
            price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.fsQm '))).text
            marcket_cap = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.hPHvUM '))).text            

            data = {
                "price": price,
                "marcket_cap": marcket_cap
            }
        except NoSuchElementException as e:
            data = {"error": str(e)}
        finally:
            driver.quit()

        return data
