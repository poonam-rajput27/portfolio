import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_quotes_data():
    """
    Scrapes dynamic quotes from quotes.toscrape.com/js/ using Selenium.
    Returns a list of dictionaries containing quotes, authors, and tags.
    """
    # Set up Chrome options to run in the background (headless mode)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Initialize the Chrome browser instance
    driver = webdriver.Chrome(options=options)
    scraped_quotes = []
    
    try:
        url = "https://quotes.toscrape.com/js/"
        print(f"Opening browser context and navigating to: {url}")
        driver.get(url)
        
        # Explicit Wait: Wait up to 10 seconds for the dynamic JavaScript components to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))
        
        # Grab all rendered quote blocks from the DOM
        quote_blocks = driver.find_elements(By.CLASS_NAME, "quote")
        
        for block in quote_blocks:
            # Extract text elements safely inside the isolated container
            text = block.find_element(By.CLASS_NAME, "text").text
            author = block.find_element(By.CLASS_NAME, "author").text
            
            # Extract tags inside the container
            tag_elements = block.find_elements(By.CLASS_NAME, "tag")
            tags = [tag.text for tag in tag_elements]
            
            # Clean text up and append to our structured payload array
            scraped_quotes.append({
                "quote": text.strip("“”"), 
                "author": author,
                "tags": tags
            })
            
        print(f"Successfully scraped {len(scraped_quotes)} dynamic elements.")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        
    finally:
        # Crucial: Always quit the browser driver session to free up system memory
        driver.quit()
        
    return scraped_quotes

# Main execution verification wrapper
if __name__ == "__main__":
    data = get_quotes_data()
    
    # Print the clean data to check the layout structure
    print("\n--- Scraped Output Data Sample ---")
    for item in data[:3]:  # Print the first 3 elements for structural validation
        print(f"Quote: \"{item['quote']}\"")
        print(f"Author: {item['author']}")
        print(f"Tags: {', '.join(item['tags'])}\n")