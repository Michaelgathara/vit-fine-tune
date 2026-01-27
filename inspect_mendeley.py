import requests
import re

url = "https://data.mendeley.com/datasets/wmfd4p3z32/1"
try:
    r = requests.get(url)
    print(r.text[:2000]) # First 2000 chars
    # Search for download link pattern
    # typically https://data.mendeley.com/public-files/datasets/{id}/files/{file_id}/file_content
    ids = re.findall(r'wmfd4p3z32', r.text)
    print(f"Found IDs count: {len(ids)}")
    
    # Check for specific file links
    links = re.findall(r'https://data.mendeley.com/public-files/datasets/[^"]+', r.text)
    print("Found links:", links)
except Exception as e:
    print(e)
