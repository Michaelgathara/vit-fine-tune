import requests
import re
import json

url = "https://data.mendeley.com/datasets/wmfd4p3z32/1"
print(f"Fetching {url}...")
r = requests.get(url)
print(f"Status: {r.status_code}")

# Look for direct file links or preloaded state
# Usually there is a script tag with JSON
matches = re.findall(r'<script>window\.__PRELOADED_STATE__ = (.*?)</script>', r.text)
if matches:
    print("Found preloaded state!")
    try:
        data = json.loads(matches[0])
        # Traverse to find files
        # structure might be dataset -> files
        dataset = data.get('dataset', {})
        files = dataset.get('files', [])
        print(f"Found {len(files)} files in metadata.")
        for f in files:
            print(f"Name: {f.get('contentDetails', {}).get('name')}")
            print(f"Download URL: {f.get('contentDetails', {}).get('downloadUrl')}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print("No preloaded state found.")
    # Print some of the HTML to see what's there
    print(r.text[:2000])
