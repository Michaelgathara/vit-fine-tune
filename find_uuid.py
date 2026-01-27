import requests
import re

url = "https://data.mendeley.com/datasets/wmfd4p3z32/1"
r = requests.get(url)

# Search for UUIDs
uuids = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', r.text)
print(f"Found {len(uuids)} UUIDs.")
for u in set(uuids):
    print(u)
