import requests
from bs4 import BeautifulSoup

def get_amazon_laptops():
    url = "https://www.amazon.in/s?k=laptop"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }

    try:
        # 10 seconds timeout taaki page ghuma na rahe
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200 and "captcha" not in response.text.lower():
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("div", {"data-component-type": "s-search-result"})
            laptop_data = []

            for item in items:
                title_tag = item.find('h2', class_='a-size-medium')
                price_tag = item.find('span', class_='a-price-whole')
                rating_tag = item.find('span', class_='a-icon-alt')
                
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    price = price_tag.get_text(strip=True) if price_tag else "N/A"
                    rating = "N/A"
                    if rating_tag:
                        raw_rating = rating_tag.get_text(strip=True)
                        rating = raw_rating.split(" ")[0] if "out of" in raw_rating else raw_rating
                    
                    laptop_data.append({
                        'Title': title,
                        'Price': price,
                        'Rating': rating,
                    })
            
            # Agar sahi data mila toh return karo
            if laptop_data:
                return laptop_data

        # ---- FALLBACK DUMMY DATA FOR TESTING ----
        # Agar Amazon ne block kiya, toh ye data screen par dikhega taaki page open ho sake!
        print("Amazon blocked us! Returning mock data for frontend testing.")
        return [
            {"Title": "HP Laptop 15s (Mock Data)", "Price": "42,990", "Rating": "4.2"},
            {"Title": "ASUS Vivobook 16 (Mock Data)", "Price": "55,000", "Rating": "4.5"},
            {"Title": "Dell Inspiron 3520 (Mock Data)", "Price": "38,400", "Rating": "4.0"}
        ]

    except Exception as e:
        print(f"Scraping error: {e}")
        # Error aane par bhi dummy data return karein taaki Flask crash na ho
        return [
            {"Title": "Sample Laptop (Error Fallback)", "Price": "00,000", "Rating": "0.0"}
        ]