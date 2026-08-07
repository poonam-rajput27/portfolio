import requests
import pandas as pd

def fetch_wikipedia_data(search_term="technology", limit=20):
    """
    Fetches Wikipedia articles metadata based on search parameters.
    Returns a dictionary formatted for consumption by the Flask application pipeline.
    """
    # Wikipedia official API endpoint
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # 1. Fetch search data directly using payload configuration
        search_payload = {
            "action": "query",
            "list": "search",
            "srsearch": search_term, 
            "format": "json",
            "utf8": 1,
            "srlimit": limit
        }

        response = requests.get(BASE_URL, params=search_payload, headers=HEADERS, timeout=20)
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API request failed with status code {response.status_code}"
            }

        search_results = response.json().get("query", {}).get("search", [])
        articles = []

        # 2. Extract baseline details without fetching the summary text
        for item in search_results:
            page_id = item.get("pageid")
            
            articles.append({
                "title": item.get("title"),
                "page_id": page_id,
                "word_count": item.get("wordcount"),
                "category": "Wikipedia Article",
                "link": f"https://en.wikipedia.org/?curid={page_id}"
            })

        # 3. Return the payload safely inside the expected data block schema
        return {
            "success": True,
            "products": articles
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Allows debugging check via local terminal run
if __name__ == "__main__":
    result = fetch_wikipedia_data(search_term="technology", limit=5)
    if result["success"]:
        df = pd.DataFrame(result["products"])
        print("\n--- Local Testing Layout Preview ---")
        print(df)
    else:
        print(f"Error occurred: {result['error']}")