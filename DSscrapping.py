import requests
from bs4 import BeautifulSoup

def scrape_quotes_to_scrape():
    base_url = "https://quotes.toscrape.com/page/{}/"
    all_quotes = []

    for i in range(1, 6):  # Pour scraper les 5 premières pages
        url = base_url.format(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            all_quotes.append({'text': text, 'author': author, 'tags': tags})

    return all_quotes

# Exécutez cette fonction et imprimez les résultats
quotes_data = scrape_quotes_to_scrape()
for quote in quotes_data:
    print(quote)

