import requests
from bs4 import BeautifulSoup

# CRITICAL: Make sure this has the 's' -> get_books_data
def get_books_data():
    url = 'https://books.toscrape.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    } 

    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        html_code = response.text
        soup = BeautifulSoup(html_code, "html.parser")
        
        items = soup.find_all("article", class_="product_pod")
        books_data = []

        for book in items:
            title_tag = book.find("h3").find("a") if book.find("h3") else None
            title = title_tag['title'] if title_tag and title_tag.has_attr('title') else "N/A"
            
            price_tag = book.find("p", class_="price_color")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            
            instock_tag = book.find("p", class_="instock availability")
            availability = instock_tag.get_text(strip=True) if instock_tag else "N/A"
            
            rating_tag = book.find("p", class_=lambda x: x and 'star-rating' in x)
            rating_text = 0
            if rating_tag and len(rating_tag['class']) > 1:
                rating_word = rating_tag['class'][1]
                rating_text = rating_map.get(rating_word, 0)

            books_data.append({
                'title': title,
                'price': price,
                'availability': availability,
                'rating': rating_text
            })
                
        return books_data

    except Exception as e:
        print(f"Scraping error: {e}")
        return []