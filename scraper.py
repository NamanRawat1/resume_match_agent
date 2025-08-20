# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def fetch_naukri_jobs(search_url, num_pages=2):
    options = Options()
    options.add_argument("--headless=new")  # newer headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    jobs = []

    for page in range(1, num_pages + 1):
        url = f"{search_url}-{page}" if page > 1 else search_url
        driver.get(url)
        time.sleep(3)  # let the page load fully

        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.select("article.jobTuple, div.jobTuple")  # handle both tag types

        # Extract all job links from listing page
        job_links = []
        for card in cards:
            title_tag = card.select_one("a.title, a.jobTitle")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            if link:
                job_links.append({"title": title, "url": link})

        # Now fetch job descriptions without going back
        for job in job_links:
            try:
                driver.get(job["url"])
                time.sleep(2)
                details = BeautifulSoup(driver.page_source, "html.parser")
                desc_tag = details.select_one("div.job-desc, div.description, section.jd-container")
                desc = desc_tag.get_text(" ", strip=True) if desc_tag else ""
                job["description"] = desc
                jobs.append(job)
            except Exception:
                job["description"] = ""
                jobs.append(job)

    driver.quit()
    return jobs
