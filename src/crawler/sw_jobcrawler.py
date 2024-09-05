from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Job
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

def JobCrawler(job_title):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service('/opt/homebrew/bin/chromedriver')  # Update with the path to your chromedriver

    # Construct the URL with the user-defined job title
    job_title_encoded = job_title.replace(" ", "+")
    url = f"https://www.remoterocketship.com/?page=1&sort=DateAdded&locations=United+States&seniority=entry-level%2Cjunior&jobTitle={job_title_encoded}"
    
    if is_url_active(url):
        print("The URL is active.")
    else:
        print("The URL is not active.")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)  # Use the dynamically constructed URL

    job_links = []
    try:
        job_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "company/") and contains(@href, "jobs") and @target="_blank"]'))
        )

        for job_element in job_elements:
            href = job_element.get_attribute('href')
            job_links.append(href)

            # Check if the job URL already exists in the database before creating
            job, created = Job.objects.get_or_create(url=href)

            # If a new job was created, populate the header and description
            if created:
                job.header = extract_header_from_link(href)  # Assuming you've defined this function
                job.description = extract_description_from_link(href)  # Assuming you've defined this function
                job.save()
    except TimeoutException:
        job_links = []  # Return an empty list if a timeout occurs

    finally:
        driver.quit()

    return job_links

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

def is_url_active(url):
    try:
        response = requests.get(url)
        # Check if the status code indicates that the URL is active
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error checking URL: {e}")
        return False