from django.shortcuts import render
from .sw_jobcrawler import JobCrawler, extract_header_from_link, extract_description_from_link
from .tw_crawler import twJobCrawler, twextract_header_from_link, twextract_description_from_link
from django.http import HttpResponse
from .models import Job, twJob


def home(request):
    return render(request, 'home.html')


def crawl_view(request):
    job_links = twJobCrawler()
    job_details = []

    for link in job_links:
        header = twextract_header_from_link(link)
        description = twextract_description_from_link(link)
        
        # Use get_or_create to avoid duplicates
        job, created = twJob.objects.get_or_create(url=link, defaults={'header': header, 'description': description})
        
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

