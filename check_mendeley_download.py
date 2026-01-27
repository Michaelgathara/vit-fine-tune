import requests

base = "https://data.mendeley.com/public-files/datasets/wmfd4p3z32"
candidates = [
    f"{base}/1/download-all.zip",
    f"{base}/1/archive.zip",
    f"{base}/download-all",
    f"https://data.mendeley.com/datasets/wmfd4p3z32/1/download",
    f"https://data.mendeley.com/api/datasets/wmfd4p3z32/1/download-all"
]

for url in candidates:
    print(f"Checking {url}...")
    try:
        r = requests.head(url)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Found it!")
            break
    except Exception as e:
        print(e)
