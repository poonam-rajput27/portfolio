import requests
import random
BASE_URL = "https://fakestoreapi.com/products"
def fetch_products():
    try:
        response = requests.get(BASE_URL, timeout=10)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API failed with status {response.status_code}"
            }

        data = response.json()

        products = []

    
        for item in random.sample(data, 8):
            products.append({
                "title": item.get("title"),
                "price": item.get("price"),
                "category": item.get("category"),
                "rating": item.get("rating", {}).get("rate"),
                "image": item.get("image")
            })

        return {
            "success": True,
            "products": products
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    result = fetch_products()
    print(result)