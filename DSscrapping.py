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
# Function to scrape quotes with a specific tag
