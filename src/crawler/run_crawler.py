from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler('http://localhost:8000/test.html')
    titles, links = crawler.crawl()
    print(titles)
    print(links)