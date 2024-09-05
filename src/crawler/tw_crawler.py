from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import twJob
import requests
from bs4 import BeautifulSoup

def twJobCrawler():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service('/opt/homebrew/bin/chromedriver')  # Update with the path to your chromedriver

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.remoterocketship.com/?page=1&sort=DateAdded&jobTitle=Technical+Writer&locations=United+States&seniority=entry-level%2Cjunior")  # Update with the target URL

    job_links = []
    try:
        job_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "company/") and contains(@href, "jobs") and @target="_blank"]'))
        )

        for job_element in job_elements:
            href = job_element.get_attribute('href')
            job_links.append(href)

            # Check if the job URL already exists in the database before creating
            job, created = twJob.objects.get_or_create(url=href)

            # If a new job was created, populate the header and description
            if created:
                job.header = twextract_header_from_link(href)  # Assuming you've defined this function
                job.description = twextract_description_from_link(href)  # Assuming you've defined this function
                job.save()

    finally:
        driver.quit()

    return job_links

def twextract_header_from_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <h1> tag with the specific class
    header_tag = soup.find('h1', class_='text-3xl font-semibold text-primary')
    
    # Extract the text content
    header = header_tag.get_text(strip=True) if header_tag else 'No header found'
    
    return header

def twextract_description_from_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <p> tags with the specific class
    paragraphs = soup.find_all('p', class_='text-secondary whitespace-pre-line')
    # Combine all text content into a single string
    description = "\n".join(p.get_text(strip=True) for p in paragraphs)
    
    return description if description else 'No description found'