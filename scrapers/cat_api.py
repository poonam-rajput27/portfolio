import requests
BASE_URL = "https://api.thecatapi.com/v1/images/search?limit=10"
def fetch_cats():

    try:

        response = requests.get(BASE_URL, timeout=10)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API failed with status {response.status_code}"
            }

        data = response.json()

        cats = []

        for item in data:

            cats.append({
                "id": item.get("id"),
                "image": item.get("url")
            })

        return {
            "success": True,
            "cats": cats
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":

    result = fetch_cats()

    print(result)