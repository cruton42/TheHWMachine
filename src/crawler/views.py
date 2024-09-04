from django.shortcuts import render
from .crawler import Crawler

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the home page!")


def crawl_view(request):
    crawler = Crawler('http://localhost:8000/test.html')
    titles, links = crawler.crawl()
    print(titles)
    print(links)
    return render(request, 'crawler.html', {'titles': titles, 'links': links})