import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    """Initializes the Chrome driver cleanly using native Selenium 4."""
    chrome_options = Options()
    
    # Crucial for avoiding immediate bot detection on Nike
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Standard stability arguments
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Custom User-Agent to look like a real browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # CLEAN INITIALIZATION: No Service() or ChromeDriverManager() needed anymore!
    driver = webdriver.Chrome(options=chrome_options)
    
    # Override navigator.webdriver to further bypass detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver

def scrape_nike_products(url, max_scrolls=3):
    """Navigates to a Nike category page, handles dynamic scrolling, and extracts items."""
    driver = init_driver()
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the main product grid to load dynamically
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

        # Handle dynamic infinite scrolling
        print("Handling dynamic scroll...")
        for i in range(max_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)  # Wait for lazy-loaded items to append to DOM
            print(f"Scrolled {i+1}/{max_scrolls} times.")

        # Extract dynamically loaded products
        products = driver.find_elements(By.CLASS_NAME, "product-card")
        print(f"\nFound {len(products)} products! Extracting data...\n")
        
        print(f"{'Title':<40} | {'Subtitle/Category':<25} | {'Price':<10}")
        print("-" * 85)

        for product in products:
            try:
                title = product.find_element(By.CLASS_NAME, "product-card__title").text.strip()
                subtitle = product.find_element(By.CLASS_NAME, "product-card__subtitle").text.strip()
                
                try:
                    price = product.find_element(By.CSS_SELECTOR, "[data-test='product-price']").text.strip()
                except:
                    price = "Price Not Found"

                print(f"{title[:38]:<40} | {subtitle[:23]:<25} | {price:<10}")
            except Exception:
                continue

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        print("\nClosing browser...")
        driver.quit()
