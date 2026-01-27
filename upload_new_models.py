import os
from huggingface_hub import HfApi, create_repo

USERNAME = "michaelgathara"
TOKEN = ""

models_to_upload = {
    "models/raf_db_finetuned": "vit-face-raf-db",
    "models/affectnet_finetuned": "vit-face-affectnet"
}

api = HfApi(token=TOKEN)

def upload_model(local_path, repo_name):
    repo_id = f"{USERNAME}/{repo_name}"
    print(f"Processing {repo_id}...")
    
    try:
        print("Creating repository...")
        create_repo(repo_id, token=TOKEN, exist_ok=True, private=False)
        
        print(f"Uploading {local_path} to {repo_id}...")
        api.upload_folder(
            folder_path=local_path,
            repo_id=repo_id,
            repo_type="model"
        )
        print(f"Successfully uploaded {repo_id}")
        
    except Exception as e:
        print(f"Error uploading {repo_id}: {e}")

if __name__ == "__main__":
    for local_path, repo_name in models_to_upload.items():
        if os.path.exists(local_path):
            upload_model(local_path, repo_name)
        else:
            print(f"Local path {local_path} not found.")
