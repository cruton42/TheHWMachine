import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def crawl(self):
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from the page
        titles = [title.text for title in soup.find_all('h1')]
        links = [link.get('href') for link in soup.find_all('a', href=True)]

        return titles, links

