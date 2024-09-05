from django.shortcuts import render, redirect, get_object_or_404
from .sw_jobcrawler import JobCrawler, extract_header_from_link, extract_description_from_link
from .tw_crawler import twJobCrawler, twextract_header_from_link, twextract_description_from_link
from django.http import HttpResponse
from .models import Job, twJob, Resume
from .forms import UploadPDFForm, UserPDF, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from .forms import CoverLetterRequestForm
from .utils import extract_text_from_pdf
from openai import OpenAI
import openai
import requests
client = OpenAI(api_key=settings.OPENAI_API_KEY)


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
    job_title = request.GET.get('job_title', 'Software Engineer')  # Default to 'Software Engineer' if no job_title provided
    job_title_encoded = requests.utils.quote(job_title)
    url = f"https://www.remoterocketship.com/?page=1&sort=DateAdded&locations=United+States&seniority=entry-level%2Cjunior&jobTitle={job_title_encoded}"

    if not is_url_active(url):
        return render(request, 'error.html', {'message': 'The URL is not active. Please try another job title.'})

    job_links = JobCrawler(job_title)  # Fetch job links using your crawler

    # Check if there are job results
    if not job_links:
        return render(request, 'error.html', {'message': 'No job results found for the given title. Please try another job title.'})

    job_details = []

    for link in job_links:
        # Extract header and description from each job link
        header = extract_header_from_link(link)
        description = extract_description_from_link(link)

        # Use get_or_create to avoid duplicates in the database
        job, created = Job.objects.get_or_create(url=link, defaults={'header': header, 'description': description})

        # Append job details with id to the list
        job_details.append({
            'id': job.id,  # Ensure job ID is included from the database
            'header': job.header,
            'link': job.url,
            'description': job.description
        })

    # Debugging: Print each job's ID and header
    for job in job_details:
        print(f"Job ID: {job['id']}, Job Header: {job['header']}")

    # Pass job details to the template for rendering
    return render(request, 'jobcrawler.html', {'jobs': job_details})

def is_url_active(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False
    

def error_view(request):
    return render(request, 'error.html')


@login_required
def upload_pdf_view(request):

    # Check if a PDF is already uploaded for the user
    existing_pdf = UserPDF.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_instance = form.save(commit=False)
            pdf_instance.user = request.user
            # Check if a PDF already exists for the user
            existing_pdf = UserPDF.objects.filter(user=request.user).first()
            if existing_pdf:
                existing_pdf.pdf_file = pdf_instance.pdf_file
                existing_pdf.save()
            else:
                pdf_instance.save()
            return redirect('success')  # Replace 'success_url' with your success page
    else:
        form = UploadPDFForm()

    # Pass the existing PDF (if any) to the template
    return render(request, 'upload_pdf.html', {
        'form': form,
        'existing_pdf': existing_pdf,  # Send the existing PDF to the template
    })


def test_gpt_4o_mini():
    try:
        # Create the completion request
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a haiku about recursion in programming."}
            ],
            max_tokens=5
        )

        # Access and print the completion content
        response_message = completion.choices[0].message.content.strip()
        print(response_message)

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")






def custom_login_view(request):
    test_gpt_4o_mini()

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

def custom_logout_view(request):
    logout(request)
    return redirect('login')

def success_view(request):
    return render(request, 'success.html')


# Set up OpenAI API key

@login_required
def generate_cover_letter(request, job_id):
    try:
        # Fetch the job from the database
        job = Job.objects.get(id=job_id)

        # Get the user's resume
        user_resume = UserPDF.objects.filter(user=request.user).first()  # Ensure the correct model is used

        if user_resume:
            # Extract text from the uploaded resume file
            resume_text = extract_text_from_pdf(user_resume.pdf_file.path)
            print(f"Resume Text: {resume_text[:500]}")
            # Generate cover letter using the AI function
            cover_letter = generate_cover_letter_with_ai(job, resume_text)
            print(f"Generated Cover Letter: {cover_letter}")
            # Render the generated cover letter
            return render(request, 'cover_letter.html', {'cover_letter': cover_letter})
        else:
            # If no resume is found, redirect to the upload resume page
            return redirect('upload_resume') 

    except Job.DoesNotExist:
        # If the job ID is not found
        messages.error(request, "The job you're trying to apply for does not exist.")
        return redirect('home')

    except Resume.DoesNotExist:
        # If the user has no resume, render a specific page or redirect them to upload
        messages.error(request, "You need to upload a resume to generate a cover letter.")
        return redirect('upload_pdf')  # Ensure you have a view for this


def generate_cover_letter_with_ai(job, resume_text):
    prompt = f"""
    Write a professional cover letter for the following job:
    
    Job Title: {job.header}
    Job Description: {job.description}
    
    Using the following resume text:
    
    {resume_text}
    
    Cover Letter:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        cover_letter = response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        cover_letter = "Error generating cover letter."

    return cover_letter




def no_resume(request):
    return render(request, 'no_resume.html')

def request_cover_letter_view(request):
    if request.method == 'POST':
        form = CoverLetterRequestForm(request.POST)
        if form.is_valid():
            job_id = form.cleaned_data['job_id']
            resume_id = form.cleaned_data['resume_id']

            job = get_object_or_404(Job, id=job_id)
            resume = get_object_or_404(Resume, id=resume_id)

            # Extract text from the PDF if not already extracted
            if not resume.text_content:
                resume.text_content = extract_text_from_pdf(resume.pdf_file.path)
                resume.save()

            cover_letter = generate_cover_letter(job, resume.text_content)

            # You can save or display the cover letter as needed
            return render(request, 'cover_letter_result.html', {'cover_letter': cover_letter})
    else:
        form = CoverLetterRequestForm()

    return redirect('some_view')  # Redirect or return to a form page
