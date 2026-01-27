import requests

urls = [
    "https://data.mendeley.com/public-api/datasets/wmfd4p3z32/1/files",
    "https://data.mendeley.com/public-api/datasets/wmfd4p3z32/versions/1/files",
    "https://data.mendeley.com/api/datasets/wmfd4p3z32/1/files"
]

for url in urls:
    print(f"Trying {url}...")
    try:
        r = requests.get(url)
        print(r.status_code)
        if r.status_code == 200:
            print(r.text[:500])
    except Exception as e:
        print(e)
