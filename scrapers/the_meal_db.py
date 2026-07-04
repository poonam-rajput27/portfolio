import requests
#BASE_URL = "https://www.themealdb.com/api/json/v1/1/random.php"
BASE_URL = "https://www.themealdb.com/api/json/v1/1/filter.php?c=Dessert"

def fetch_cookie_recipes():
    try:
        response = requests.get(BASE_URL, timeout=10)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API failed with status {response.status_code}"
            }

        data = response.json()

        recipes = []

        if data["meals"]:
            for meal in data["meals"]:
                recipes.append({
                    "name": meal.get("strMeal"),
                    "category": meal.get("strCategory"),
                    "area": meal.get("strArea"),
                    "image": meal.get("strMealThumb")
                })

        return {
            "success": True,
            "recipes": recipes
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    result = fetch_cookie_recipes()
    print(result)