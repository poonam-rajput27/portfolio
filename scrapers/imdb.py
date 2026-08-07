import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    """Initializes the Chrome driver cleanly using native Selenium 4 with anti-detection flags."""
    chrome_options = Options()
    
    # Avoid immediate bot detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Standard stability arguments
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Custom User-Agent to look like a real browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    # Override navigator.webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver

def scrape_imdb_movies(url="https://www.imdb.com/chart/top/", limit=20):
    """Navigates to IMDb Top Charts, handles dynamic content, and extracts movie data."""
    driver = init_driver()
    movie_list = []
    
    try:
        print(f"Navigating to IMDb: {url}")
        driver.get(url)
        
        # Wait for the main movie list grid/list items to load
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")))

        # Scroll slightly to trigger any lazy-loaded elements if needed
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(1.5)

        # Find all movie row elements
        movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
        print(f"Found {len(movies)} elements. Extracting top {limit} movies...")

        for index, movie in enumerate(movies[:limit]):
            try:
                # Extract title block
                title_element = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text")
                raw_title = title_element.text.strip()
                
                # IMDb titles usually look like "1. The Shawshank Redemption" -> clean the rank out
                title = raw_title.split('.', 1)[-1].strip() if '.' in raw_title else raw_title
                
                # Extract Rating (e.g., 9.3)
                try:
                    rating_element = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating")
                    rating = rating_element.text.strip()
                except:
                    rating = "N/A"
                
                # Extract Metadata details (Year, Duration, etc.)
                metadata_items = movie.find_elements(By.CSS_SELECTOR, "span.sc-b189961a-8.kLaxFE")
                year = metadata_items[0].text.strip() if len(metadata_items) > 0 else "N/A"
                duration = metadata_items[1].text.strip() if len(metadata_items) > 1 else "N/A"

                # Append data as dictionary matching your Flask pipeline format
                movie_list.append({
                    "rank": index + 1,
                    "title": title,
                    "rating": rating,
                    "year": year,
                    "duration": duration
                })
                
            except Exception as e:
                # Skip any row that drops a field due to structural updates
                continue

    except Exception as e:
        print(f"An error occurred during IMDb scraping: {e}")
        
    finally:
        print("Closing browser...")
        driver.quit()
        
    return movie_list

if __name__ == "__main__":
    # Test block to verify it runs standalone
    data = scrape_imdb_movies(limit=10)
    print("\n--- Scraped Results ---")
    for m in data:
        print(f"#{m['rank']} - {m['title']} ({m['year']}) | Rating: {m['rating']} | Duration: {m['duration']}")