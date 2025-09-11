# Importing required libraries
import requests  # To send HTTP requests
from bs4 import BeautifulSoup  # To parse and extract data from HTML
import pandas as pd  # To store and handle scraped data in tabular form

# User-Agent and Accept-Language headers (helps avoid request blocking by website)
headers = {
    'User-Agent': 'Your_User_Agent_Here',
    'Accept-Language': 'en-us,en;q=0.5'
}

def scrape_reviews_and_save_to_csv(url, product_name):
    """
    Scrapes review information from Flipkart and saves it to a CSV file.
    """
    customer_names = []
    review_title = []
    ratings = []
    comments = []

    # Looping through pages 1 to 43 (total 43 pages to scrape)
    for i in range(1, 44):
        # Add page number to the URL
        current_url = f"{url}&page={i}"

        # Make a GET request to fetch the page
        page = requests.get(current_url, headers=headers)

        # Parse page content using BeautifulSoup
        soup = BeautifulSoup(page.content, 'html.parser')

        # ----- Extract customer names -----
        names = soup.find_all('p', class_='_2sc7ZR')
        for name in names:
            customer_names.append(name.get_text(strip=True))

        # ----- Extract review titles -----
        titles = soup.find_all('p', class_='_2-N8zT')
        for title in titles:
            review_title.append(title.get_text(strip=True))

        # ----- Extract ratings -----
        ratings_all = soup.find_all('div', class_='col _2wzgFH K0kLPL')
        for rating in ratings_all:
            ratings.append(rating.div.text.strip())

        # ----- Extract review comments -----
        comments_all = soup.find_all('div', class_='t-ZTKy')
        for comment in comments_all:
            comment_text = comment.div.div.get_text(strip=True)
            comments.append(comment_text)

    # Ensure all columns have equal length (necessary before creating DataFrame)
    min_length = min(len(customer_names), len(review_title), len(ratings), len(comments))
    customer_names = customer_names[:min_length]
    review_title = review_title[:min_length]
    ratings = ratings[:min_length]
    comments = comments[:min_length]

    # Create DataFrame from scraped data
    data = {
        'Customer Name': customer_names,
        'Review Title': review_title,
        'Rating': ratings,
        'Comment': comments
    }
    df = pd.DataFrame(data)

    # Save DataFrame to CSV file
    df.to_csv(f'{product_name}_reviews.csv', index=False)

# URLs for scraping reviews
badminton_url = "https://www.flipkart.com/yonex-mavis-350-nylon-shuttle-yellow/product-reviews/itmfcjdyhnghfyey?pid=STLEFJ7UFQGRUUR3&lid=LSTSTLEFJ7UFQGRUUR3SUDA2S&marketplace=FLIPKART"
motorola_url = "https://www.flipkart.com/motorola-g84-5g-viva-magneta-256-gb/product-reviews/itmed938e33ffdf5?pid=MOBGQFX672GDDQAQ&lid=LSTMOBGQFX672GDDQAQSSIAM2&marketplace=FLIPKART"

# Scrape and save reviews for badminton product
scrape_reviews_and_save_to_csv(badminton_url, 'badminton')

# Scrape and save reviews for Motorola product
scrape_reviews_and_save_to_csv(motorola_url, 'motorola')



