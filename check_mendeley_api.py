import requests

url = "https://data.mendeley.com/public-api/datasets/wmfd4p3z32/files"
try:
    r = requests.get(url)
    print(r.status_code)
    print(r.text)
except Exception as e:
    print(e)
