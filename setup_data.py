import os
import requests
import zipfile
import tarfile
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
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

def extract_file(filepath, extract_to):
    print(f"Extracting {filepath} to {extract_to}...")
    if filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif filepath.endswith('.tar.gz') or filepath.endswith('.tgz'):
        with tarfile.open(filepath, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    else:
        print(f"Unknown archive format: {filepath}")

def setup_zenodo():
    print("Setting up Zenodo dataset...")
    zenodo_id = "7963451"
    api_url = f"https://zenodo.org/api/records/{zenodo_id}"
    
    try:
        r = requests.get(api_url)
        r.raise_for_status()
        data = r.json()
        
        # Find the zip file or main dataset file
        files = data.get('files', [])
        if not files:
            print("No files found in Zenodo record.")
            return

        os.makedirs("data/zenodo", exist_ok=True)
        
        for file_info in files:
            file_url = file_info['links']['self']
            filename = file_info['key']
            target_path = os.path.join("data", filename)
            
            if not os.path.exists(target_path):
                print(f"Downloading {filename}...")
                download_file(file_url, target_path)
            
            extract_file(target_path, "data/zenodo")
            
    except Exception as e:
        print(f"Error setting up Zenodo dataset: {e}")

def setup_mendeley():
    print("Setting up Mendeley dataset...")
    # Mendeley Data API or direct link structure
    # Using the dataset ID wmfd4p3z32 version 1
    # Often the download link is https://data.mendeley.com/public-files/datasets/{id}/files/{file_id}/file_content
    # But simpler is usually to look for the "download all" link or specific file links if known.
    # We will try to fetch the dataset metadata first.
    
    # Mendeley doesn't have a simple public JSON API like Zenodo for file listing without auth sometimes, 
    # but let's try a known pattern or scraping if needed. 
    # Actually, for Mendeley Data, the URL is https://data.mendeley.com/datasets/wmfd4p3z32/1
    # We might need to manually find the link or use a library if available. 
    # Let's try to search for the direct download link pattern.
    
    # Assuming we can find a direct zip link or list of files. 
    # For now, let's try to hit the page and find the download link if we can't find a direct API.
    # However, to be robust, let's try a direct download URL structure if possible.
    
    # Fallback: User provided link https://data.mendeley.com/datasets/wmfd4p3z32/1
    # Let's try to get the metadata from the API
    
    try:
        # This is a guess at the API endpoint, otherwise we might need to parse HTML
        # https://data.mendeley.com/api/datasets/wmfd4p3z32/1
        # If this works, we can get file lists.
        
        # It seems Mendeley API is https://data.mendeley.com/public-api/datasets/wmfd4p3z32/files
        r = requests.get("https://data.mendeley.com/public-api/datasets/wmfd4p3z32/files")
        
        if r.status_code == 200:
             files = r.json()
             os.makedirs("data/mendeley", exist_ok=True)
             for f in files:
                 # Download each file
                 # Url is typically in 'contentDetails' -> 'downloadUrl'
                 # Or construct it
                 pass
                 # ... implementation to be filled after checking if this API works
        else:
            print("Could not access Mendeley API.")
            
    except Exception as e:
        print(f"Error setting up Mendeley dataset: {e}")

if __name__ == "__main__":
    setup_zenodo()
    # setup_mendeley() # Will implement after verification
