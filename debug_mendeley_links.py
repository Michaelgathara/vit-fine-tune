import requests
import re

url = "https://data.mendeley.com/datasets/wmfd4p3z32/1"
r = requests.get(url)

# Search for hrefs
hrefs = re.findall(r'href="([^"]+)"', r.text)
for h in hrefs:
    if 'download' in h or 'zip' in h:
        print(f"Candidate link: {h}")

# Also look for API calls in the JS bundles if possible, but that's hard.
# Let's try to construct the API URL again but with a different endpoint.
# Maybe https://data.mendeley.com/api/datasets/wmfd4p3z32/1 returns the metadata including files?
# We tried that in check_mendeley_api_v2.py and it returned metadata but maybe we missed the file list.
