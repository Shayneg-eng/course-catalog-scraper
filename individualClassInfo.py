import json
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

with open("Academic-Catalog.json") as f:
    catalog = json.load(f)

paths = []

def walk(node):
    if "Path" in node:
        paths.append(node["Path"])
    for child in node.get("Children", []):
        walk(child)

walk(catalog)

def to_public_url(path):
    return "https://elon.smartcatalogiq.com/en" + path.lower()

output_lock = Lock()

def fetch_and_save(path):
    url = to_public_url(path)
    try:
        html = requests.get(url, timeout=30).text
        result = {"url": url, "length": len(html), "status": "success"}
    except Exception as e:
        result = {"url": url, "length": 0, "status": "error", "error": str(e)}
    
    with output_lock:
        with open("course_data.json", "a") as f:
            json.dump(result, f)
            f.write("\n")
    
    print(result["url"], result.get("length", 0))
    return result

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(fetch_and_save, path) for path in paths]
    for future in futures:
        future.result()