import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36',
    'Accept-Language': 'en-us,en;q=0.5'
}

def scrape_reviews_and_save_to_csv(url, product_name, max_pages=50):
    customer_names, review_title, ratings, comments = [], [], [], []

    for i in range(1, max_pages+1):
        current_url = f"{url}&page={i}"
        print(f"Scraping page {i}...")

        page = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        reviews = soup.find_all('div', class_='col _2wzgFH K0kLPL')
        if not reviews:  # stop if no reviews found
            break

        try:
            customer_names.extend([n.get_text(strip=True) for n in soup.find_all('p', class_='_2sc7ZR')])
            review_title.extend([t.get_text(strip=True) for t in soup.find_all('p', class_='_2-N8zT')])
            ratings.extend([r.get_text(strip=True) for r in soup.find_all('div', class_='_3LWZlK _1BLPMq')])
            comments.extend([c.div.div.get_text(strip=True) for c in soup.find_all('div', class_='t-ZTKy')])
        except Exception as e:
            print(f"Error on page {i}: {e}")

        time.sleep(1)  # polite scraping

    min_length = min(len(customer_names), len(review_title), len(ratings), len(comments))
    df = pd.DataFrame({
        'Customer Name': customer_names[:min_length],
        'Review Title': review_title[:min_length],
        'Rating': ratings[:min_length],
        'Comment': comments[:min_length]
    })

    filename = f'{product_name}_reviews.csv'
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} reviews to {filename}")
    return df

