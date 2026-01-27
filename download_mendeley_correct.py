import requests
from tqdm import tqdm
import zipfile
import os

def download_and_extract():
    url = "https://data.mendeley.com/public-files/datasets/wmfd4p3z32/files/97369cf8-edb4-4f47-a803-0380c640b31e/file_downloaded"
    output_zip = "data/mendeley_cropped.zip"
    extract_to = "data/mendeley_extracted"
    
    # Check if already downloaded
    if not os.path.exists(output_zip):
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_zip, 'wb') as f:
            pbar = tqdm(total=total_size, unit='iB', unit_scale=True)
            for chunk in response.iter_content(chunk_size=1024*1024): # 1MB chunks
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
            pbar.close()
    else:
        print("Zip file already exists.")
        
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
