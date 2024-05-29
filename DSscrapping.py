import requests
from bs4 import BeautifulSoup
import csv

# URL de base et chemin de connexion
base_url = 'https://quotes.toscrape.com'
login_url = 'https://quotes.toscrape.com/login'

# Détails du compte
username = 'nayla'
password = '123'

# Démarrer une session
session = requests.Session()

# Récupérer la page de connexion pour obtenir le token CSRF
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

# Créer les données de la requête de connexion
login_data = {
    'csrf_token': csrf_token,
    'username': username,
    'password': password,
}

# Envoyer la requête de connexion
session.post(login_url, data=login_data)

# Supposons que le token que vous voulez est stocké dans un cookie
# Nous utiliserons un cookie de session comme exemple
token = session.cookies.get('session_token')  # Ajustez selon le vrai nom du cookie

# Écrire le token dans un fichier CSV
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Token'])
    writer.writerow([token])
