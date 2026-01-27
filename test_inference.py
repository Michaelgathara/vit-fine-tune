import torch
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import os

def run_example():
    # Use a sample image from the test set
    image_path = "data/zenodo_processed/test/happy/frame0_Chandler_happy.jpg"
    
    if not os.path.exists(image_path):
        print("Image not found, please check path.")
        return

    print(f"Loading image from {image_path}...")
    image = Image.open(image_path).convert("RGB")
    
    # Load model
    repo_name = "michaelgathara/vit-face-zenodo"
    print(f"Loading model from {repo_name}...")
    
    try:
        processor = ViTImageProcessor.from_pretrained(repo_name)
        model = ViTForImageClassification.from_pretrained(repo_name)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Prepare inputs
    inputs = processor(images=image, return_tensors="pt")
    
    # Inference
    print("Running inference...")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        predicted_label = model.config.id2label[predicted_class_idx]
        
    print(f"Predicted emotion: {predicted_label}")
    print(f"True label (from filename): happy")

if __name__ == "__main__":
    run_example()
