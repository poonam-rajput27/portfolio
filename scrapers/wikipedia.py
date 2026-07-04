import requests
import json

# Wikipedia official search API endpoint
BASE_URL = "https://en.wikipedia.org/w/api.php"

def fetch_wikipedia_data():
    try:
        # Configuration parameters for searching articles
        payload = {
            "action": "query",
            "list": "search",
            "srsearch": "technology", 
            "format": "json",
            "utf8": 1,
            "srlimit": 5 
        }
        
        # A completely standard browser User-Agent to guarantee it doesn't hang or block
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # Reduced timeout to 5 seconds so it breaks immediately if there's a connection issue
        response = requests.get(BASE_URL, params=payload, headers=headers, timeout=5)
        
        # Status check
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API failed with status {response.status_code}"
            }
            
        data = response.json()
        search_results = data.get("query", {}).get("search", [])
        
        articles = []
        for item in search_results:
            page_id = item.get("pageid")
            articles.append({
                "title": item.get("title"),
                "page_id": page_id,
                "word_count": item.get("wordcount"),
                "category": "Wikipedia Article",
                "link": f"https://en.wikipedia.org/?curid={page_id}"
            })
            
        return {
            "success": True,
            "products": articles
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }
