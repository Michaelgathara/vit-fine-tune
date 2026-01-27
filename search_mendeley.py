import requests
import urllib.parse

query = "Genuine and Fake Facial Emotion Dataset (GFFD-2025)"
encoded = urllib.parse.quote(query)
url = f"https://data.mendeley.com/api/datasets?search={encoded}"
print(f"Searching {url}...")

try:
    r = requests.get(url)
    print(r.status_code)
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, dict) and 'results' in data: # Guessing structure
             print(f"Found {len(data['results'])} results.")
        else:
             print(data) # Print structure to understand
except Exception as e:
    print(e)
