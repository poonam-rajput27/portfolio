from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_yahoo_finance():

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    url = "https://finance.yahoo.com/markets/stocks/most-active/"
    driver.get(url)

    time.sleep(30)

    stocks = []

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for row in rows[:30]:

        try:
            symbol = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        except:
            symbol = ""

        try:
            company = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        except:
            company = ""

        try:
            price = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
        except:
            price = ""

        try:
            change = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
        except:
            change = ""

        try:
            volume = row.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
        except:
            volume = ""

        stocks.append({
            "symbol": symbol,
            "company": company,
            "price": price,
            "change": change,
            "volume": volume
        })

    driver.quit()

    return stocks