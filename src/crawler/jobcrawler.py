from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def JobCrawler():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service('/opt/homebrew/bin/chromedriver')  # Update with the path to your chromedriver

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.remoterocketship.com/")  # Update with the target URL

    job_links = []
    try:
        job_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "jobs/") and @target="_blank"]'))
        )

        for job_element in job_elements:
            href = job_element.get_attribute('href')
            job_links.append(href)

    finally:
        driver.quit()

    return job_links