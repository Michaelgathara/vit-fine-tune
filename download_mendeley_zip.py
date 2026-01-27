import requests
from tqdm import tqdm
import zipfile
import os

def download_and_extract():
    url = "https://data.mendeley.com/api/datasets/wmfd4p3z32/1/download-all"
    output_zip = "data/mendeley_all.zip"
    extract_to = "data/mendeley_extracted"
    
    print(f"Downloading from {url}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_zip, 'wb') as f:
        pbar = tqdm(total=total_size, unit='iB', unit_scale=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
        pbar.close()
        
    print("Extracting...")
    os.makedirs(extract_to, exist_ok=True)
    try:
        with zipfile.ZipFile(output_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Done.")
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid zip file.")

if __name__ == "__main__":
    download_and_extract()
