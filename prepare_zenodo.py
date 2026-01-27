import os
import shutil
from tqdm import tqdm

def prepare_split(source_dir, target_base_dir):
    print(f"Processing {source_dir} -> {target_base_dir}")
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist!")
        return

    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    for emo in emotions:
        os.makedirs(os.path.join(target_base_dir, emo), exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.jpg') and 'frame' in file:
                try:
                    parts = file.replace('.jpg', '').split('_')
                    emotion = parts[-1].lower()
                    
                    if emotion in emotions:
                        src_path = os.path.join(root, file)
                        dst_path = os.path.join(target_base_dir, emotion, file)
                        shutil.copy2(src_path, dst_path)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

def main():
    base_zenodo = "data/zenodo/IFEED_Base"
    processed_dir = "data/zenodo_processed"
    prepare_split(os.path.join(base_zenodo, "Training"), os.path.join(processed_dir, "train"))
    prepare_split(os.path.join(base_zenodo, "Testing"), os.path.join(processed_dir, "test"))

if __name__ == "__main__":
    main()
