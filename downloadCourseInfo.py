import requests

url = "https://elon.smartcatalogiq.com/Institutions/Elon-University/json/2025-2026/Academic-Catalog.json"
data = requests.get(url, timeout=30).json()

with open("Academic-Catalog.json", "w") as f:
    import json
    json.dump(data, f, indent=2)