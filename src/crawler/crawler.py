import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def crawl(self):
        titles = []
        links = []
        try:
            response = self.session.get(self.url)
            response.raise_for_status()  # Check for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract data from the page
            titles = [title.text for title in soup.find_all('h1')]
            links = [link.get('href') for link in soup.find_all('a', href=True)]

            # Follow links to crawl deeper
            for link in links:
                if link.startswith('http'):
                    titles_deep, links_deep = self.crawl(link)
                    titles.extend(titles_deep)
                    links.extend(links_deep)

        except requests.RequestException as e:
            print(f"Error occurred: {e}")

        return titles, links