import os
import shutil
from tqdm import tqdm
from glob import glob
import random

SOURCE_DATASETS = {
    "zenodo": "data/zenodo_processed",
    "mendeley": "data/mendeley_processed",
    "raf_db": "data/raf_db",
    "affectnet": "data/affectnet"
}

OUTPUT_DIR = "data/combined"
LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

LABEL_MAP = {
    'anger': 'angry',
    'happiness': 'happy',
    'sadness': 'sad',
    'Angry': 'angry',
    'Disgust': 'disgust',
    'Fear': 'fear',
    'Happy': 'happy',
    'Sad': 'sad',
    'Surprise': 'surprise',
    'Neutral': 'neutral'
}

def normalize_label(label):
    return LABEL_MAP.get(label, label).lower()

def merge_datasets():
    if os.path.exists(OUTPUT_DIR):
        print(f"Removing existing {OUTPUT_DIR}...")
        shutil.rmtree(OUTPUT_DIR)
    
    print(f"Creating {OUTPUT_DIR}...")
    
    for split in ['train', 'test']:
        for label in LABELS:
            os.makedirs(os.path.join(OUTPUT_DIR, split, label), exist_ok=True)
            
    stats = {split: {label: 0 for label in LABELS} for split in ['train', 'test']}
    
    for ds_name, ds_path in SOURCE_DATASETS.items():
        print(f"Processing {ds_name}...")
        
        splits = [d for d in os.listdir(ds_path) if os.path.isdir(os.path.join(ds_path, d))]
        
        for split in splits:
            target_split = 'train' if split == 'train' else 'test'
            
            split_path = os.path.join(ds_path, split)
            if not os.path.exists(split_path):
                continue
                
            label_dirs = [d for d in os.listdir(split_path) if os.path.isdir(os.path.join(split_path, d))]
            
            for label_dir in label_dirs:
                norm_label = normalize_label(label_dir)
                if norm_label not in LABELS:
                    continue
                    
                src_label_path = os.path.join(split_path, label_dir)
                dst_label_path = os.path.join(OUTPUT_DIR, target_split, norm_label)
                
                files = glob(os.path.join(src_label_path, "*.*"))
                
                for f in tqdm(files, desc=f"{ds_name}/{split}/{norm_label}", leave=False):
                    filename = os.path.basename(f)
                    new_filename = f"{ds_name}_{split}_{filename}"
                    shutil.copy2(f, os.path.join(dst_label_path, new_filename))
                    stats[target_split][norm_label] += 1

    print("\n--- Combined Dataset Statistics ---")
    for split in stats:
        print(f"\n{split.upper()}:")
        total = 0
        for label, count in stats[split].items():
            print(f"  {label}: {count}")
            total += count
        print(f"  TOTAL: {total}")

if __name__ == "__main__":
    merge_datasets()
