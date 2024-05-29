import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_filtered_quotes():
    base_url = "https://quotes.toscrape.com/page/{}/"
    selected_tags = {'love', 'inspirational', 'life', 'humor'}
    all_quotes = []

    for page in range(1, 6):  
        response = requests.get(base_url.format(page))
        soup = BeautifulSoup(response.text, 'html.parser')
        
        quotes = soup.find_all('div', class_='quote')
        
        for quote in quotes:
            text = quote.find('span', class_='text').text
            tags = {tag.text for tag in quote.find_all('a', class_='tag')}
            if tags & selected_tags:  
                all_quotes.append({'text': text, 'tags': ', '.join(tags & selected_tags)})

    # écrire dans un fichier CSV
    df = pd.DataFrame(all_quotes)
    df.to_csv('results.csv', index=False)

scrape_filtered_quotes()
