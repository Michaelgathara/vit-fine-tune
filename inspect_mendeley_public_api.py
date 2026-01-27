import requests
import json

url = "https://data.mendeley.com/public-api/datasets/wmfd4p3z32"
r = requests.get(url)
data = r.json()

print(json.dumps(data, indent=2))
