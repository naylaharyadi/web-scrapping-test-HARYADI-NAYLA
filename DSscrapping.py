import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    base_url = "https://quotes.toscrape.com/page/{}/"
    selected_tags = {"love", "inspirational", "life", "humor"}
    all_quotes = []

    for page in range(1, 6):  # Scrape les 5 premières pages
        url = base_url.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        
        for quote in quotes:
            text = quote.find('span', class_='text').text
            tags = {tag.text for tag in quote.find_all('a', class_='tag')}
            
            # Filtrer pour ne garder que les citations ayant des tags sélectionnés
            if tags & selected_tags:
                all_quotes.append({'quote': text, 'tags': list(tags & selected_tags)})

    return all_quotes

# Exécutez cette fonction et affichez les résultats dans un tableau
quotes_data = scrape_quotes()
for quote in quotes_data:
    print(quote)


