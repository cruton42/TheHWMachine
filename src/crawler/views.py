from django.shortcuts import render, redirect
from .sw_jobcrawler import JobCrawler, extract_header_from_link, extract_description_from_link
from .tw_crawler import twJobCrawler, twextract_header_from_link, twextract_description_from_link
from django.http import HttpResponse
from .models import Job, twJob
from .forms import UserPDFForm, UserPDF, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


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

@login_required
def upload_pdf_view(request):
    if request.method == 'POST':
        form = UserPDFForm(request.POST, request.FILES)
        if form.is_valid():
            user_pdf, created = UserPDF.objects.get_or_create(user=request.user)
            user_pdf.pdf = form.cleaned_data['pdf']
            user_pdf.save()
            return redirect('success')  # Redirect to a success page or wherever you want
    else:
        form = UserPDFForm()

    return render(request, 'upload_pdf.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to a home page or another page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')