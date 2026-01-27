import requests

candidates = [
    "36bac695-2fcf-4978-88f6-afbcd708e679",
    "a2567f1b-8a60-4464-b725-6c59f84a5801",
    "d6f58a8e-fef9-4d7b-9b57-c3a5b69c7961"
]

for uuid in candidates:
    print(f"Checking {uuid}...")
    url = f"https://data.mendeley.com/public-api/datasets/{uuid}/files"
    try:
        r = requests.get(url)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print(r.text[:500])
    except Exception as e:
        print(e)
        
    url2 = f"https://data.mendeley.com/api/datasets/{uuid}"
    try:
        r = requests.get(url2)
        print(f"API Status: {r.status_code}")
        if r.status_code == 200:
            print(r.text[:500])
    except Exception as e:
        print(e)
