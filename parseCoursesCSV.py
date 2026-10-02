import json
import requests
import csv
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Read course_data.json
with open("course_data.json") as f:
    course_entries = [json.loads(line) for line in f if line.strip()]

# Filter only successful entries
successful_urls = [entry["url"] for entry in course_entries if entry["status"] == "success"]

csv_lock = Lock()
csv_file = "courses.csv"

# Initialize CSV with headers
fieldnames = ["URL", "Course Code", "Title", "Description", "Credits", "Prerequisites", "Course Types", "Previous Course Number"]

def parse_course_page(url):
    try:
        html = requests.get(url, timeout=30).text
        soup = BeautifulSoup(html, 'html.parser')
        
        course_code = ""
        title = ""
        description = ""
        credits = ""
        prerequisites = ""
        course_types = ""
        previous_course_number = ""
        
        # Extract course code and title from h1
        h1 = soup.find('h1')
        if h1:
            # Course code is in a span tag, title is the rest
            span = h1.find('span')
            if span:
                course_code = span.get_text(strip=True)
                # Remove the span to get the title
                span.decompose()
                title = h1.get_text(strip=True)
            else:
                # Fallback if no span
                h1_text = h1.get_text(strip=True)
                parts = h1_text.split(None, 1)
                course_code = parts[0] if parts else ""
                title = parts[1] if len(parts) > 1 else ""
        
        # Extract description from div with class "desc"
        desc_div = soup.find('div', class_='desc')
        if desc_div:
            desc_p = desc_div.find('p')
            if desc_p:
                description = desc_p.get_text(strip=True)
        
        # Extract credits from div with class "sc_credits"
        credits_div = soup.find('div', class_='sc_credits')
        if credits_div:
            credits_content = credits_div.find('div', class_='credits')
            if credits_content:
                credits = credits_content.get_text(strip=True)
        
        # Extract prerequisites from div with class "sc_prereqs"
        prereqs_div = soup.find('div', class_='sc_prereqs')
        if prereqs_div:
            # Get all text except the h2 header
            h2 = prereqs_div.find('h2')
            if h2:
                h2.decompose()
            prerequisites = prereqs_div.get_text(strip=True)
        
        # Extract course types from div with class "sc-Attributes"
        attributes_div = soup.find('div', class_='sc-Attributes')
        if attributes_div:
            # Get all text except the h3 header
            h3 = attributes_div.find('h3')
            if h3:
                h3.decompose()
            course_types = attributes_div.get_text(strip=True)
        
        # Extract previous course number from div with class "extra"
        extra_div = soup.find('div', class_='extra')
        if extra_div:
            # Get all text except the h3 header
            h3 = extra_div.find('h3')
            if h3:
                h3.decompose()
            previous_course_number = extra_div.get_text(strip=True)
        
        result = {
            "URL": url,
            "Course Code": course_code,
            "Title": title,
            "Description": description,
            "Credits": credits,
            "Prerequisites": prerequisites,
            "Course Types": course_types,
            "Previous Course Number": previous_course_number
        }
        
        # Write to CSV
        with csv_lock:
            with open(csv_file, "a", newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(result)
        
        print(f"[OK] {url}")
        return result
    except Exception as e:
        print(f"[ERROR] {url}: {str(e)}")
        return None

# Initialize CSV file with headers
with open(csv_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

# Process all URLs with 10 workers
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(parse_course_page, url) for url in successful_urls]
    for future in futures:
        future.result()

print(f"\nDone! Results saved to {csv_file}")
