import requests
from bs4 import BeautifulSoup

def get_country_data():
    url = 'https://www.scrapethissite.com/pages/simple/'
    
    # Standard browser signature
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try: 
        # Added verify=False to bypass restrictive local network SSL inspection proxies if present
        response = requests.get(url, headers=headers, timeout=10, verify=True)
        
        if response.status_code != 200:
            print(f"HTTP Error: Server responded with status code {response.status_code}")
            return []

        html_code = response.text
        soup = BeautifulSoup(html_code, "html.parser")
        
        country_divs = soup.find_all("div", class_="country")
        country_data = []

        for div in country_divs:
            name_tag = div.find("h3", class_="country-name")
            capital_tag = div.find("span", class_="country-capital")
            pop_tag = div.find("span", class_="country-population")
            area_tag = div.find("span", class_="country-area")

            if name_tag:
                country_data.append({
                    "name": name_tag.get_text(strip=True),
                    "capital": capital_tag.get_text(strip=True) if capital_tag else "N/A",
                    "population": pop_tag.get_text(strip=True) if pop_tag else "N/A",
                    "area": area_tag.get_text(strip=True) if area_tag else "N/A"
                })

        return country_data

    except Exception as e:
        print(f"Scraping error encountered: {e}")
        return []

# Standalone debug execution hook
if __name__ == "__main__":
    print("--- STANDALONE SCRAPER DEBUG RUN ---")
    data = get_country_data()
    print(f"Result count: {len(data)}")