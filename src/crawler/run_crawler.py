from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler('http://example.com')
    titles, links = crawler.crawl()
    print(titles)
    print(links)