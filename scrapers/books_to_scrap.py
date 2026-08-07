import requests
from bs4 import BeautifulSoup

def get_book_data():
    url = 'http://books.toscrape.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Dictionary to convert written string ratings to numbers for looping in Jinja
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Failed to fetch books. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Locate all individual book container cards
        book_elements = soup.find_all("article", class_="product_pod")
        book_data = []

        for book in book_elements:
            # 1. Extract Title (from the 'title' attribute of the nested <a> tag)
            title_tag = book.find("h3").find("a") if book.find("h3") else None
            title = title_tag['title'] if title_tag and title_tag.has_attr('title') else "N/A"
            
            # 2. Extract Price
            price_tag = book.find("p", class_="price_color")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            
            # 3. Extract Availability status text
            instock_tag = book.find("p", class_="instock availability")
            availability = instock_tag.get_text(strip=True) if instock_tag else "N/A"
            
            # 4. Extract Star Rating class (e.g., class="star-rating Three")
            rating_tag = book.find("p", class_=lambda x: x and 'star-rating' in x)
            rating_text = 0  # Default fallback rating
            if rating_tag and len(rating_tag['class']) > 1:
                rating_word = rating_tag['class'][1] # This gets 'One', 'Two', etc.
                rating_text = rating_map.get(rating_word, 0)

            # Keep keys consistently lowercase to match the HTML design pattern
            book_data.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating_text
            })

        return book_data

    except Exception as e:
        print(f"Books scraping error: {e}")
        return []

# Standalone check execution block
if __name__ == "__main__":
    print("--- RUNNING STANDALONE BOOKS SCRAPER TEST ---")
    books = get_book_data()
    print(f"Total books parsed: {len(books)}")
    if books:
        print("Sample Item Data extracted successfully:\n", books[0])
    else:
        print("Failed to pull down book data.")