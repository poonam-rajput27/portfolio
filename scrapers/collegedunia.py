import requests
from bs4 import BeautifulSoup

def colleges():
    url = "https://collegedunia.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        html_code = response.text
        soup = BeautifulSoup(html_code, "html.parser")
        
        table = soup.find("table")
        if not table:
            return []  # Return empty list if no table found
            
        rows = table.find_all("tr")
        college_data = []

        # FIX: Loop over 'rows' instead of the function name 'colleges'
        for row in rows:
            # FIX: Search inside the current 'row' object
            title_tag = row.find('div', class_='jsx-831255015 text-dark college-name')
            fee_tag = row.find('div', class_='jsx-831255015 fees text-dark')
            rating_tag = row.find('span', class_='jsx-831255015 text-dark rating')
            
            # Check if title exists to avoid processing blank header rows
            if title_tag:
                # FIX: Clean the data using .get_text() so it returns text, not HTML tags
                title = title_tag.get_text(strip=True)
                fee = fee_tag.get_text(strip=True) if fee_tag else "N/A"
                rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"
                
                college_data.append({
                    'Title': title,
                    'fee': fee,
                    'rating': rating,
                })
                
        # FIX: Return your collected data list, not the function name!
        return college_data

    except Exception as e:
        print(f"Scraping error: {e}")
        return []