import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    """Initializes Chrome driver with clean settings to bypass simple blocks."""
    chrome_options = Options()
    
    # Automation bypass flags
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Performance & Stability flags
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Mask browser identity
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver

def scrape_yahoo_finance(url="https://finance.yahoo.com/trending-tickers/"):
    """Scrapes trending tickers dynamically from Yahoo Finance and returns a list of data."""
    driver = init_driver()
    scraped_data = []
    
    try:
        print(f"Navigating to Yahoo Finance: {url}")
        driver.get(url)
        
        # Wait for the main dynamic table body to load completely
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        
        # Smooth brief scroll down to load any dynamic components or lazy tables
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(2)
        
        # Target table rows matching stock records
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        print(f"Found {len(rows)} financial tickers. Parsing data...\n")
        
        for row in rows:
            try:
                # Scrape elements using robust relative CSS selectors
                symbol = row.find_element(By.CSS_SELECTOR, "td[data-field='symbol']").text.strip()
                name = row.find_element(By.CSS_SELECTOR, "td[data-field='longName']").text.strip()
                price = row.find_element(By.CSS_SELECTOR, "td[data-field='regularMarketPrice']").text.strip()
                change = row.find_element(By.CSS_SELECTOR, "td[data-field='regularMarketChangePercent']").text.strip()
                
                # Append to our structured list
                scraped_data.append({
                    "symbol": symbol,
                    "name": name,
                    "price": price,
                    "change": change
                })
                
            except Exception:
                # If an arbitrary row structure differs, skip it safely
                continue
                
    except Exception as e:
        print(f"Scraping Error: {e}")
        
    finally:
        print("Closing Yahoo Finance automation session...")
        driver.quit()
        
    return scraped_data

if __name__ == "__main__":
    # Test block to verify your script standalone
    data = scrape_yahoo_finance()
    print(f"\nSuccessfully collected {len(data)} items:")
    for item in data[:5]:  # Display first 5 items as a preview
        print(f"{item['symbol']} | {item['name'][:25]} | Price: {item['price']} | Change: {item['change']}")