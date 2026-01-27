import os
from huggingface_hub import HfApi

# Configuration
USERNAME = "michaelgathara"
TOKEN = ""

api = HfApi(token=TOKEN)

repos = {
    "models/zenodo_finetuned/README.md": "vit-face-zenodo",
    "models/mendeley_finetuned/README.md": "vit-face-mendeley"
}

for local_path, repo_name in repos.items():
    repo_id = f"{USERNAME}/{repo_name}"
    print(f"Uploading README to {repo_id}...")
    try:
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="model"
        )
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")
