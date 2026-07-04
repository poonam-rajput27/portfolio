from flask import Flask, render_template
from scrapers.collegedunia import colleges
from scrapers.amazon_laptops import get_amazon_laptops
from scrapers.countriesofworld import get_country_data
from scrapers.flipkart_shoes import get_flipkart_shoes
from scrapers.books_to_scrap import get_book_data
from scrapers.yahoofinance import scrape_yahoo_finance
from scrapers.indeed import scrape_indeed_jobs
from scrapers.the_meal_db import fetch_cookie_recipes
from scrapers.wikipedia import fetch_wikipedia_data
from scrapers.fake_store_api import fetch_products
from scrapers.json_placeholder import fetch_posts
from scrapers.cat_api import fetch_cats
from scrapers.quotes import get_quotes_data
from scrapers.nike import scrape_nike_products
# Add this alongside your other dynamic scrapers at the top of app.py
from scrapers.imdb import scrape_imdb_movies
app = Flask(__name__)

# 1. Main Landing Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/learnMore')
def learn_more():
    return render_template('learnMore.html')

# 2. Project / Static Pages
@app.route('/static')
def static_page():
    return render_template('static.html')

@app.route('/minor1')
def minor1():
    return render_template('minor1.html')

@app.route('/minor2')
def minor2():
    return render_template('minor2.html')

# 3. Scraping Dashboard Page
@app.route('/scraping')
def scraping():
    return render_template('scraping.html')

@app.route('/scraping_static')
def scraping_static():
    return render_template('scraping_static.html')
@app.route("/dynamicscraping")
def dynamicscraping():
    return render_template("dynamicscraping.html")


@app.route("/apiscraping")
def api_scraping():

    return render_template("apiscraping.html")

# 4. CollegeDunia Scraper Route
@app.route('/static/collegedunia')
def scraping_static_collegedunia():
    scraped_data = colleges()
    return render_template("collegedunia.html", colleges=scraped_data)

# 5. Amazon Scraper
#  Route (ISKO HUMNE FIX KIYA HAI)
@app.route('/static/amazon_laptops')
def scraping_static_amazon():
    # 1. Fire up the amazon parsing function 
    scraped_data = get_amazon_laptops()
    
    # 2. Return the template safely and pass data to Jinja engine
    return render_template("amazon_laptops.html", laptops=scraped_data)
@app.route('/static/countriesofworld')
def scraping_static_countries():
    # 1. countriesofworld.py ke get_country_data() function ko call kiya
    scraped_countries = get_country_data()
    
    # 2. Template render kiya aur 'countries' variable ko pass kiya
    return render_template("countriesofworld.html", countries=scraped_countries)


@app.route('/static/flipkart_shoes')
def scraping_static_flipkart_shoes():
    scraped_shoes = get_flipkart_shoes()
    return render_template("flipkart_shoes.html", shoes=scraped_shoes)
# 6. Books to Scrape Route (Updated function name)
# 6. Books to Scrape Route
@app.route('/static/books_to_scrap')
def scraping_static_books():
    # 1. Calls the function from scrapers/books_to_scrap.py
    scraped_books = get_book_data()
    
    # 2. Renders the template. Make sure this filename matches your actual file!
    return render_template("books_to_scrap.html", books=scraped_books)
@app.route("/mealdb")
def mealdb():

    result = fetch_cookie_recipes()

    if result["success"]:
        return render_template(
            "the_meal_db.html",
            recipes=result["recipes"]
        )

    return render_template(
        "the_meal_db.html",
        error=result["error"]
    )
@app.route("/wikipedia")
def wikipedia_route():  
    result = fetch_wikipedia_data()
    if result["success"]:
        return render_template("wikipedia.html", products=result["products"])
    return render_template("wikipedia.html", error=result["error"])
    return jsonify(["technology", "python", "web scraping"])
@app.route("/fakestore")
def fakestore():

    result = fetch_products()

    if result["success"]:
        return render_template(
            "fake_store_api.html",
            products=result["products"]
        )

    return render_template(
        "fake_store_api.html",
        error=result["error"]
    )
@app.route("/json_placeholder")
def jsonplaceholder():

    result = fetch_posts()

    if result["success"]:
        return render_template(
            "json_placeholder.html",
            posts=result["posts"]
        )

    return render_template(
        "json_placeholder.html",
        error=result["error"])
@app.route("/catapi")
def catapi():

    result = fetch_cats()

    if result["success"]:
        return render_template(
            "cat_api.html",
            cats=result["cats"]
        )

    return render_template(
        "cat_api.html",
        error=result["error"])
    # ==========================================================================
# Quotes to Scrape - Dynamic Selenium Route
# ==========================================================================

@app.route("/quotes")
def quotes_route():
    try:
        # 1. Scraper function ko call karke dynamic data load karein
        scraped_quotes = get_quotes_data()
        
        # 2. Agar data mil jata hai, toh use template mein bhej dein
        return render_template("quotes.html", quotes=scraped_quotes)
        
    except Exception as e:
        # 3. Fallback handle karein agar backend scraping mein error aaye
        print(f"Routing Error on /quotes: {e}")
        return render_template("quotes.html", quotes=[], error=str(e))
@app.route("/nike-scraping")
def nike_store():
    try:
        # Pass the URL explicitly so the scraper knows where to go
        scraped_products = scrape_nike_products("https://www.nike.com/w/mens-new-3n82z76xr0g", max_scrolls=3)
        return render_template("nike.html", products=scraped_products)
        
    except Exception as e:
        print(f"Routing Error on /nike_store: {e}")
        return render_template("index.html", products=[], error=str(e))
@app.route("/yahoofinance")
def yahoo_finance_route():
    try:
        # Calls your new Yahoo Finance dynamic Selenium scraper
        stock_data = scrape_yahoo_finance()
        
        # Renders the finance.html dashboard template with live data
        return render_template("yahoo_finance.html", stocks=stock_data)
    except Exception as e:
        print(f"Routing Error on /yahoo_finance: {e}")
        return render_template("yahoo_finance.html", stocks=[], error=str(e))
@app.route("/indeed")
def scrape_indeed_job():
    try:
        # Default query parameters for our automated extraction pipeline
        job_data = scrape_indeed_jobs("Python Developer", "Remote")
        return render_template("jobs.html", jobs=job_data)
    except Exception as e:
        print(f"Routing Error on /indeed_parser: {e}")
        return render_template("jobs.html", jobs=[], error=str(e))
# ==========================================================================
# IMDb Top Charts - Dynamic Selenium Route
# ==========================================================================

@app.route("/imdb")
def imdb_route():
    try:
        # 1. Run the scraper to get the top 20 movies dynamically
        scraped_movies = scrape_imdb_movies(limit=20)
        
        # 2. Render the new template and pass the data
        return render_template("imdb.html", movies=scraped_movies)
        
    except Exception as e:
        # 3. Fallback gracefully if Selenium hits an error
        print(f"Routing Error on /imdb: {e}")
        return render_template("imdb.html", movies=[], error=str(e))

# ==================== SERVER LAUNCH ================
    
if __name__ == '__main__':
    app.run(debug=True, port=5003)
    