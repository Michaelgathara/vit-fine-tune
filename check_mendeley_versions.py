import requests

urls = [
    "https://data.mendeley.com/api/datasets/wmfd4p3z32",
    "https://data.mendeley.com/api/datasets/wmfd4p3z32/versions/1",
    "https://data.mendeley.com/api/datasets/wmfd4p3z32/1", # We tried this and it returned search results
    "https://data.mendeley.com/public-api/datasets/wmfd4p3z32",
    "https://data.mendeley.com/public-api/datasets/wmfd4p3z32/versions/1"
]

for url in urls:
    print(f"Checking {url}...")
    try:
        r = requests.get(url)
        print(r.status_code)
        if r.status_code == 200:
            print(r.text[:500])
    except Exception as e:
        print(e)
