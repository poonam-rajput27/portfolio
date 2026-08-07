# C:\Users\poonam rajput\Documents\GitHub\portfolio\scrapers\indeed.py
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
def scrape_indeed_jobs(job_title="Python Developer", location="Remote"):
    """
    Robust Indeed Job Scraper with fault-tolerant individual column tracking.
    """
    options = Options()
    
    # Normal window layout helps glide past Cloudflare perimeter filters automatically.
    # If this runs successfully on your machine, you can change to options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Inject real desktop environment profiles to decouple default automated signatures
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    # Clear automation navigator variables
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    parsed_jobs = []
    
    try:
        # Build structured query parameters
        formatted_title = job_title.replace(" ", "+")
        formatted_loc = location.replace(" ", "+")
        target_url = f"https://www.indeed.com/jobs?q={formatted_title}&l={formatted_loc}"
        
        print(f"[INFO] Initializing browser target sequence to: {target_url}")
        driver.get(target_url)
        
        # Give JS dynamic components ample time to render listing columns
        time.sleep(5)
        
        # Explicit Wait: Confirm job container nodes are injected into viewport DOM
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon")))
        
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
        print(f"[SUCCESS] Discovered {len(job_cards)} job cards available on page.")
        
        rank_counter = 1
        for card in job_cards:
            if rank_counter > 15:  # Cap pull output to the top 15 results
                break
                
            # Initialize structured mapping block defaults for this job row
            job_record = {
                "Rank": rank_counter,
                "Title": "Not Disclosed",
                "Company": "Confidential Employer",
                "Location": "Not Specified",
                "Salary": "Not Disclosed",
                "URL": "None"
            }
            
            # --- Field 1: Job Title Extraction ---
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span[id^='jobTitle-']")
                job_record["Title"] = title_el.text.strip()
            except:
                try:
                    # Fallback backup selector path for varying A/B test UI models
                    job_record["Title"] = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text.strip()
                except:
                    pass
            
            # --- Field 2: Company Name Extraction ---
            try:
                # Target primary custom structural test attribute tag
                company_el = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']")
                job_record["Company"] = company_el.text.strip()
            except:
                try:
                    job_record["Company"] = card.find_element(By.CSS_SELECTOR, "span.css-63beeb").text.strip()
                except:
                    pass
                    
            # --- Field 3: Job Location Extraction ---
            try:
                location_el = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']")
                job_record["Location"] = location_el.text.strip()
            except:
                try:
                    job_record["Location"] = card.find_element(By.CSS_SELECTOR, "div.css-1p0nf51").text.strip()
                except:
                    pass

            # --- Field 4: Estimated Salary Extraction ---
            salary_selectors = [
                "div.metadata.salarySnippet-container",
                "div.metadata.estimatedSalary-container",
                "div.salary-snippet-container",
                "div.css-18v9vux"
            ]
            for selector in salary_selectors:
                try:
                    salary_el = card.find_element(By.CSS_SELECTOR, selector)
                    job_record["Salary"] = salary_el.text.strip()
                    break # Break custom tracking cascade once text content string captures cleanly
                except:
                    continue

            # --- Field 5: Core Listing Link Extraction ---
            try:
                link_el = card.find_element(By.CSS_SELECTOR, "a.jcs-JobTitle")
                job_record["URL"] = link_el.get_attribute("href")
            except:
                pass
            
            # Save whatever content blocks successfully evaluated
            parsed_jobs.append(job_record)
            rank_counter += 1

    except Exception as e:
        print(f"[CRITICAL ERROR] Core pipeline pipeline failure: {e}")
        
    finally:
        print("[INFO] Shutting down selenium tracking engine threads safely...")
        driver.quit()
        
    return parsed_jobs