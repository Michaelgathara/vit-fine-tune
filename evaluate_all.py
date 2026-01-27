import os
import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from transformers import ViTImageProcessor, ViTForImageClassification
from datasets import load_dataset
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tqdm import tqdm
import numpy as np

MODELS = {
    "Base (Fer2013)": "trpakov/vit-face-expression",
    "Fine-tuned (Zenodo)": "michaelgathara/vit-face-zenodo",
    "Fine-tuned (Mendeley)": "michaelgathara/vit-face-mendeley",
    "Fine-tuned (RAF-DB)": "michaelgathara/vit-face-raf-db",
    "Fine-tuned (AffectNet)": "michaelgathara/vit-face-affectnet"
}

DATASETS = {
    "Zenodo": "data/zenodo_processed",
    "Mendeley": "data/mendeley_processed",
    "RAF-DB": "data/raf_db",
    "AffectNet": "data/affectnet"
}

COMMON_LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

LABEL_MAPPING = {
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
    return LABEL_MAPPING.get(label, label).lower()

def load_data(dataset_name, data_dir):
    print(f"Loading {dataset_name} from {data_dir}...")
    try:
        if os.path.exists(os.path.join(data_dir, "test")):
            dataset = load_dataset("imagefolder", data_dir=data_dir, split="test")
        elif os.path.exists(os.path.join(data_dir, "validation")):
             dataset = load_dataset("imagefolder", data_dir=data_dir, split="validation")
        else:
             dataset = load_dataset("imagefolder", data_dir=data_dir, split="test")
             
        return dataset
    except Exception as e:
        print(f"Error loading {dataset_name}: {e}")
        return None

def evaluate_model(model_name, repo_id, dataset_name, dataset):
    print(f"Evaluating {model_name} on {dataset_name}...")
    
    try:
        processor = ViTImageProcessor.from_pretrained(repo_id)
        model = ViTForImageClassification.from_pretrained(repo_id)
        model.eval()
        
        id2label = model.config.id2label
        
        true_labels = []
        pred_labels = []
        
        for item in tqdm(dataset, desc=f"Eval {model_name} on {dataset_name}"):
            image = item['image'].convert("RGB")
            true_label_idx = item['label']
            true_label_name = dataset.features['label'].int2str(true_label_idx)
            normalized_true = normalize_label(true_label_name)
            
            if normalized_true not in COMMON_LABELS:
                continue

            inputs = processor(images=image, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
            
            logits = outputs.logits
            pred_idx = logits.argmax(-1).item()
            pred_label_name = id2label[pred_idx]
            normalized_pred = normalize_label(pred_label_name)
            
            true_labels.append(normalized_true)
            pred_labels.append(normalized_pred)
            
        return true_labels, pred_labels
        
    except Exception as e:
        print(f"Error evaluating {model_name}: {e}")
        return [], []

def plot_confusion_matrix(true_labels, pred_labels, title, filename):
    cm = confusion_matrix(true_labels, pred_labels, labels=COMMON_LABELS, normalize='true')
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='.2f', cmap='Blues', xticklabels=COMMON_LABELS, yticklabels=COMMON_LABELS)
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main():
    os.makedirs("results", exist_ok=True)
    results = []
    
    loaded_datasets = {}
    for name, path in DATASETS.items():
        ds = load_data(name, path)
        if ds:
            loaded_datasets[name] = ds
            
    for model_name, repo_id in MODELS.items():
        for dataset_name, dataset in loaded_datasets.items():
            true, pred = evaluate_model(model_name, repo_id, dataset_name, dataset)
            
            if not true:
                continue
                
            acc = accuracy_score(true, pred)
            report = classification_report(true, pred, output_dict=True, zero_division=0)
            
            cm_filename = f"results/cm_{model_name.replace(' ', '_').replace('(', '').replace(')', '')}_{dataset_name}.png"
            plot_confusion_matrix(true, pred, f"{model_name} on {dataset_name}", cm_filename)
            
            results.append({
                "Model": model_name,
                "Dataset": dataset_name,
                "Accuracy": acc,
                "Macro F1": report['macro avg']['f1-score'],
                "Weighted F1": report['weighted avg']['f1-score'],
                "Precision (Weighted)": report['weighted avg']['precision'],
                "Recall (Weighted)": report['weighted avg']['recall']
            })
            
    df = pd.DataFrame(results)
    df.to_csv("results/evaluation_summary.csv", index=False)
    print("\n--- Evaluation Summary ---")
    print(df.to_markdown(index=False))

if __name__ == "__main__":
    main()
