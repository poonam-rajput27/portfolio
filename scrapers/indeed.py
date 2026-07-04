import time
import random
from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def init_driver():
    """Initializes Chrome with optimized stealth headers to look like a standard user."""
    chrome_options = Options()
    
    # Crucial bypass flags for job search platforms
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Stability and sizing settings
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Modern realistic user agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Clear automation fingerprints
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver

def scrape_indeed_jobs(job_title="Python Developer", location="Remote"):
    """Searches and parses active job postings from Indeed via user simulation."""
    driver = init_driver()
    parsed_jobs = []
    
    # Construct a clean query URL to jump directly to listings safely
    formatted_title = job_title.replace(" ", "+")
    formatted_loc = location.replace(" ", "+")
    target_url = f"https://www.indeed.com/jobs?q={formatted_title}&l={formatted_loc}"
    
    try:
        print(f"Navigating to Indeed Search URL...")
        driver.get(target_url)
        
        # Humanize interaction: Explicit randomized pause to let layout components initialize
        time.sleep(random.uniform(3.5, 5.0))
        
        # Target individual dynamic card elements using structural CSS attributes
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon")))
        
        # Collect loaded job summary layout blocks
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
        print(f"Detected {len(job_cards)} job listing segments. Processing elements...\n")
        
        for card in job_cards:
            try:
                # 1. Pull Title (Nested inside structural anchor tags)
                title_element = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span")
                title = title_element.text.strip()
                
                # 2. Pull Company Name 
                company_element = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']")
                company = company_element.text.strip()
                
                # 3. Pull Location Details
                location_element = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']")
                job_location = location_element.text.strip()
                
                # 4. Pull Salary metadata cleanly (Optional column fallback)
                try:
                    salary_element = card.find_element(By.CSS_SELECTOR, "div.metadata.salarySnippet-container")
                    salary = salary_element.text.strip()
                except:
                    try:
                        salary_element = card.find_element(By.CSS_SELECTOR, "div.metadata.estimatedSalary-container")
                        salary = salary_element.text.strip()
                    except:
                        salary = "Salary Not Disclosed"
                
                # Structure matching your multi-pipeline routing standards
                parsed_jobs.append({
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "salary": salary
                })
                
            except Exception:
                # Safely slide over isolated edge-case parsing anomalies
                continue
                
    except Exception as e:
        print(f"Indeed Extraction Session Interrupt: {e}")
        
    finally:
        print("Terminating automation engine pipeline safely...")
        driver.quit()
        
    return parsed_jobs

# --- FLASK WEB ROUT