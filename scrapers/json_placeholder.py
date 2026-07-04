import requests
BASE_URL = "https://jsonplaceholder.typicode.com/posts"
def fetch_posts():
    try:
        response = requests.get(BASE_URL, timeout=10)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API failed with status {response.status_code}"
            }

        data = response.json()

        posts = []

        # Fetch first 5 posts
        for item in data[:5]:
            posts.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "body": item.get("body"),
                "userId": item.get("userId")
            })

        return {
            "success": True,
            "posts": posts
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    result = fetch_posts()

    if result["success"]:
        for post in result["posts"]:
            print("-" * 50)
            print(f"Post ID : {post['id']}")
            print(f"User ID : {post['userId']}")
            print(f"Title   : {post['title']}")
            print(f"Body    : {post['body']}")
    else:
        print(result["error"])