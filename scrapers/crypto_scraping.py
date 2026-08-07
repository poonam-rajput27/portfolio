import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_live_crypto_prices():
    print("Initializing Selenium for CoinGecko Live Crypto Tracker...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        url = "https://www.coingecko.com/"
        print(f"Navigating to live data source: {url}")
        driver.get(url)
        
        print("Waiting for dynamic crypto grid to render rows...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        
        # Scroll to load hidden DOM items
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(30)
        
        crypto_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        print(f"Successfully discovered {len(crypto_rows)} rows on the page.\n")
        
        crypto_list = []
        rank_counter = 1
        
        for row in crypto_rows:
            if rank_counter > 30:  # Limits to top 10 items
                break
            try:
                # Target name safely using robust class text lookups
                name_el = row.find_element(By.CSS_SELECTOR, "span.tw-font-bold, td.coin-name, [data-coin-name]")
                coin_name = name_el.text.strip().split("\n")[0]
                
                # Fetch asset symbol shorthand
                try:
                    ticker_el = row.find_element(By.CSS_SELECTOR, "span.tw-text-gray-400, .coin-symbol")
                    coin_ticker = ticker_el.text.strip().upper()
                except:
                    coin_ticker = "META"

                # Fetch price
                price_el = row.find_element(By.CSS_SELECTOR, "span[data-price-target], td.td-price, td.tw-text-right")
                coin_price = price_el.text.strip()
                
                # Fetch 24h change status
                try:
                    change_el = row.find_element(By.CSS_SELECTOR, "td.td-change24h, span[data-percentage-target], td[data-sort]")
                    price_change = change_el.text.strip()
                except:
                    price_change = "0.00%"
                
                if coin_name and coin_price:
                    crypto_list.append({
                        "rank": rank_counter,
                        "name": coin_name,
                        "ticker": coin_ticker,
                        "price": coin_price,
                        "trend": price_change
                    })
                    rank_counter += 1
                    
            except Exception as e:
                continue 
                
        driver.quit()
        return crypto_list
        
    except Exception as e:
        print(f"Scraping Error Trace: {e}")
        if 'driver' in locals():
            driver.quit()
        return []

if __name__ == "__main__":
    crypto_data = scrape_live_crypto_prices()
    
    if crypto_data:
        print(f"Extracted {len(crypto_data)} items successfully.")
        # Overwrite the data.json file inside the exact same folder as your dashboard file
        with open('data.json', 'w') as json_file:
            json.dump(crypto_data, json_file, indent=4)
        print("[SUCCESS] Live data saved to data.json")
    else:
        print("[ERROR] No data extracted from the source page.")