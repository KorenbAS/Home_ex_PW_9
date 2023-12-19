import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')

    quotes_data = []

    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tag_divs = quote.find('div', class_='tags')
        tags = [tag.get_text() for tag in tag_divs.find_all('a', class_='tag')]

        quotes_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    return quotes_data

def scrape_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    authors = soup.find_all('div', class_='quote')

    authors_data = []

    for author in authors:
        author_name = author.find('small', class_='author').get_text()
        author_url = url + author.find('a')['href']

        # Отримуємо додаткові дані про автора
        author_response = requests.get(author_url)
        author_soup = BeautifulSoup(author_response.text, 'html.parser')

        birth_date = author_soup.find('span', class_='author-born-date').get_text()
        birth_location = author_soup.find('span', class_='author-born-location').get_text()
        description = author_soup.find('div', class_='author-description').get_text()

        authors_data.append({
            'name': author_name,
            'birth_date': birth_date,
            'birth_location': birth_location,
            'description': description
        })

    return authors_data

quotes_data = scrape_quotes('http://quotes.toscrape.com')
authors_data = scrape_authors('http://quotes.toscrape.com')

with open('quotes.json', 'w') as f:
    json.dump(quotes_data, f, indent=4)

with open('authors.json', 'w') as f:
    json.dump(authors_data, f, indent=4)