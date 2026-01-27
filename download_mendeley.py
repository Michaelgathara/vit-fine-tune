import requests
import os
from tqdm import tqdm

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

def main():
    api_url = "https://data.mendeley.com/api/datasets/wmfd4p3z32/1/files"
    output_dir = "data/mendeley"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching file list from {api_url}...")
    r = requests.get(api_url)
    if r.status_code != 200:
        print(f"Failed to fetch files: {r.status_code}")
        return
        
    data = r.json()
    # Structure seems to be data -> results -> list of files
    # or direct list depending on exact endpoint response (previous output showed {"data":{"results":...}})
    
    files = data.get('data', {}).get('results', [])
    if not files and isinstance(data, list):
        files = data
        
    print(f"Found {len(files)} files.")
    
    for f in files:
        file_id = f.get('id')
        filename = f.get('name')
        # Content URI might be different, let's try to construct it or find it
        # content_details = f.get('contentDetails', {})
        # download_url = content_details.get('downloadUrl')
        
        # Based on typical Mendeley API, download URL is often:
        # https://data.mendeley.com/public-files/datasets/{dataset_id}/files/{file_id}/file_content
        # But we need to be sure.
        
        # Let's check if 'downloadUrl' is in the file object
        download_url = f.get('contentDetails', {}).get('downloadUrl')
        
        if not download_url:
            # Fallback construction
            download_url = f"https://data.mendeley.com/public-files/datasets/wmfd4p3z32/files/{file_id}/file_content"
            
        print(f"Downloading {filename}...")
        target_path = os.path.join(output_dir, filename)
        try:
            download_file(download_url, target_path)
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    main()
