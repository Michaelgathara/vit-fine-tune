import requests
import json

url = "https://data.mendeley.com/api/datasets/wmfd4p3z32/1"
try:
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        print("Keys:", data.keys())
        # Check for files
        if 'files' in data:
            print(f"Found {len(data['files'])} files directly.")
        elif 'data' in data:
             print("Checking 'data' key...")
             subdata = data['data']
             if isinstance(subdata, dict):
                 print("Keys in data:", subdata.keys())
                 if 'files' in subdata:
                     print(f"Found {len(subdata['files'])} files in data.")
                 if 'results' in subdata:
                     print("Checking results...")
                     print(subdata['results'])
    else:
        print(f"Status: {r.status_code}")
except Exception as e:
    print(e)
