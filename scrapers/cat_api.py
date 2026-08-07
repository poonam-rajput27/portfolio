import json
import requests
import pandas as pd

def fetch_cat_api_data():
    # 1. Fetch a list of Cat Breeds from the API
    breeds_url = "https://api.thecatapi.com/v1/breeds"
    # 2. Fetch random cat image records
    images_url = "https://api.thecatapi.com/v1/images/search?limit=10"
    
    try:
        # Fetch breeds data
        response_breeds = requests.get(breeds_url, timeout=30)
        response_breeds.raise_for_status()
        breeds_data = response_breeds.json()
        
        # Save raw JSON data to file
        with open("cat_breeds.json", "w", encoding="utf-8") as f:
            json.dump(breeds_data, f, indent=4)
            
        # Convert to Pandas DataFrame for analysis
        df_breeds = pd.json_normalize(breeds_data)
        df_breeds.to_csv("cat_breeds.csv", index=False)
        
        print(" Successfully fetched Cat Breeds data!")
        print(f" Total Breeds Found: {len(breeds_data)}")
        print("\n--- Preview of Breeds Data ---")
        print(df_breeds[['id', 'name', 'origin', 'temperament', 'life_span']].head())
        
        # Fetch random cat images
        response_images = requests.get(images_url, timeout=30)
        response_images.raise_for_status()
        images_data = response_images.json()
        
        print("\n--- Sample Cat Image URLs ---")
        for img in images_data[:3]:
            print(f"Image ID: {img['id']} | URL: {img['url']}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from The Cat API: {e}")

if __name__ == "__main__":
    fetch_cat_api_data()