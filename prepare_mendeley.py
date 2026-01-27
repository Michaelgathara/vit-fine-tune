import os
import shutil
import random
from tqdm import tqdm

def prepare_mendeley():
    source_root = "data/mendeley_extracted/CroppedDataset"
    target_root = "data/mendeley_processed"
    
    emotions = [d for d in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, d))]
    
    print(f"Found emotions: {emotions}")
    
    for emo in emotions:
        print(f"Processing {emo}...")
        all_images = []
        emo_path = os.path.join(source_root, emo)
        
        types = ["Fake", "Genuine"]
        for t in types:
            type_path = os.path.join(emo_path, t)
            if os.path.exists(type_path):
                files = os.listdir(type_path)
                for f in files:
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        all_images.append(os.path.join(type_path, f))
                        
        random.shuffle(all_images)
        split_idx = int(len(all_images) * 0.8)
        train_imgs = all_images[:split_idx]
        test_imgs = all_images[split_idx:]
        
        for img_path in train_imgs:
            dst_dir = os.path.join(target_root, "train", emo.lower())
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(img_path, os.path.join(dst_dir, os.path.basename(img_path)))
            
        for img_path in test_imgs:
            dst_dir = os.path.join(target_root, "test", emo.lower())
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(img_path, os.path.join(dst_dir, os.path.basename(img_path)))

if __name__ == "__main__":
    prepare_mendeley()
