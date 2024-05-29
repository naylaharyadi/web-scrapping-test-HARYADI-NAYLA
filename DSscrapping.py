import requests
from bs4 import BeautifulSoup
import pandas as pd
# Function to login and get the token
def login_and_get_token():
    login_url = "https://quotes.toscrape.com/login"
    # Initial request to get the CSRF token
    session = requests.Session()
    initial_response = session.get(login_url)
    soup = BeautifulSoup(initial_response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    # Login payload with CSRF token
    payload = {
        'username': 'test',
        'password': 'test',
        'csrf_token': csrf_token
    }
    login_response = session.post(login_url, data=payload)
    if login_response.status_code == 200:
        return session, csrf_token
    else:
        raise Exception("Login failed")
session, token = login_and_get_token()
# Write token to results.csv
with open('results.csv', 'w') as file:
    file.write(f"token\n{token}\n")
print("Token has been written to 'results.csv'.")

def scrape_tagged_quotes(session, tag, pages=2):
    base_url = f"https://quotes.toscrape.com/tag/{tag}/page/{{}}/"
    quotes = []
    for page_num in range(1, pages + 1):
        url = base_url.format(page_num)
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for quote in soup.select('div.quote'):
            text = quote.find('span', class_='text').get_text(strip=True)
            author = quote.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })
    return quotes
# Scrape the first 2 pages of quotes with the 'books' tag
tag = 'books'
book_quotes = scrape_tagged_quotes(session, tag, pages=2)
# Function to filter out duplicate quotes
def filter_duplicates(quotes):
    seen = set()
    filtered_quotes = []
    for quote in quotes:
        text = quote['text']
        if text not in seen:
            seen.add(text)
            filtered_quotes.append(quote)
    return filtered_quotes
# Filter out duplicate quotes
unique_book_quotes = filter_duplicates(book_quotes)
# Append quotes to results.csv
df_quotes = pd.DataFrame(unique_book_quotes, columns=['text', 'author', 'tags'])
df_quotes.to_csv('results.csv', mode='a', index=False, header=True)
print("Unique book quotes have been appended to 'results.csv'.")