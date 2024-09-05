from django.shortcuts import render
from .crawler import Crawler
from .sw_jobcrawler import JobCrawler, extract_header_from_link, extract_description_from_link
from django.http import HttpResponse
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
        
        # Use get_or_create to avoid duplicates
        job, created = Job.objects.get_or_create(url=link, defaults={'header': header, 'description': description})
        
        # Only append to job_details if the job was newly created or already exists
        job_details.append({
            'header': job.header,  # Use job.header from the database
            'link': job.url,
            'description': job.description
        })

        for job in job_details:
            print(f"Job Header: {job['header']}, Job URL: {job['link']}")

    # Pass the job details to the template for rendering
    return render(request, 'jobcrawler.html', {'jobs': job_details})

