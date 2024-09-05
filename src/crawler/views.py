from django.shortcuts import render
from .crawler import Crawler
from .sw_jobcrawler import JobCrawler
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import Job


def home(request):
    return render(request, 'home.html')


def crawl_view(request):
    crawler = Crawler('https://www.remoterocketship.com/')
    titles, links = crawler.crawl()
    print(titles)
    print(links)
    return render(request, 'crawler.html', {'titles': titles, 'links': links})

#def jobcrawl_view(request):
    job_links = JobCrawler()

    for link in job_links:
        # Example of scraping the job header and description
        header = extract_header_from_link(link)  # Replace with actual extraction logic
        description = extract_description_from_link(link)  # Replace with actual extraction logic
        
        # Save job to the database
        Job.objects.create(url=link, header=header, description=description)
    
    links_html = "<br>".join([f'<a href="{link}" target="_blank">{link}</a>' for link in job_links])
    return HttpResponse(links_html)

def jobcrawl_view(request):
    job_links = JobCrawler()
    job_details = []

    for link in job_links:
        header = extract_header_from_link(link)
        description = extract_description_from_link(link)
        
        # Save job to the database
        Job.objects.get_or_create(url=link, defaults={'header': header, 'description': description})
        
        # Append job details to the list
        job_details.append({
            'header': header,
            'link': link,
            'description': description
        })

    # Generate HTML for displaying job details
    html_content = ""
    for job in job_details:
        html_content += f'<h1 class="job-header">{job["header"]}</h1>'
        html_content += f'<a href="{job["link"]}" target="_blank">{job["link"]}</a><br>'
        html_content += f'<p class="job-description">{job["description"]}</p><br>'

    return HttpResponse(html_content)

def extract_header_from_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <h1> tag with the specific class
    header_tag = soup.find('h1', class_='text-3xl font-semibold text-primary')
    
    # Extract the text content
    header = header_tag.get_text(strip=True) if header_tag else 'No header found'
    
    return header

def extract_description_from_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <p> tags with the specific class
    paragraphs = soup.find_all('p', class_='text-secondary whitespace-pre-line')
    # Combine all text content into a single string
    description = "\n".join(p.get_text(strip=True) for p in paragraphs)
    
    return description if description else 'No description found'