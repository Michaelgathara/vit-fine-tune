import os
from datasets import load_dataset
from tqdm import tqdm

def save_dataset_to_disk(dataset_name, output_dir):
    print(f"Processing {dataset_name} -> {output_dir}...")
    
    try:
        ds = load_dataset(dataset_name)
        print(f"Splits: {ds.keys()}")
        
        if 'train' in ds:
            features = ds['train'].features
        else:
            features = ds[list(ds.keys())[0]].features
            
        labels = features['label'].names
        print(f"Labels: {labels}")
        
        for split in ds.keys():
            print(f"Saving split: {split}...")
            split_dir = os.path.join(output_dir, split)
            
            for label in labels:
                os.makedirs(os.path.join(split_dir, label), exist_ok=True)
            
            for i, item in enumerate(tqdm(ds[split])):
                image = item['image']
                label_idx = item['label']
                label_name = labels[label_idx]
                
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                image_path = os.path.join(split_dir, label_name, f"{split}_{i}.jpg")
                image.save(image_path)
                
    except Exception as e:
        print(f"Error processing {dataset_name}: {e}")

def main():
    save_dataset_to_disk("deanngkl/raf-db-7emotions", "data/raf_db")
    save_dataset_to_disk("deanngkl/affectnet_no_contempt", "data/affectnet")

if __name__ == "__main__":
    main()
