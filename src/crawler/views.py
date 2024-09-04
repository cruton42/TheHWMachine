from django.shortcuts import render
from .crawler import Crawler
from .jobcrawler import JobCrawler
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')


def crawl_view(request):
    crawler = Crawler('https://www.remoterocketship.com/')
    titles, links = crawler.crawl()
    print(titles)
    print(links)
    return render(request, 'crawler.html', {'titles': titles, 'links': links})

def jobcrawl_view(request):
    job_links = JobCrawler()
    links_html = "<br>".join([f'<a href="{link}" target="_blank">{link}</a>' for link in job_links])
    return HttpResponse(links_html)