import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from transformers import ViTImageProcessor, ViTForImageClassification
from datasets import load_dataset
from tqdm import tqdm

# Configuration
MODELS = {
    "Base (Fer2013)": "trpakov/vit-face-expression",
    "Fine-tuned (Universal)": "michaelgathara/vit-face-universal",
    "Fine-tuned (Zenodo)": "michaelgathara/vit-face-zenodo",
    "Fine-tuned (Mendeley)": "michaelgathara/vit-face-mendeley"
}

DATASETS = {
    "Zenodo": "data/zenodo_processed",
    "Mendeley": "data/mendeley_processed"
}

LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
N_CLASSES = len(LABELS)

LABEL_MAPPING = {
    'anger': 'angry', 'happiness': 'happy', 'sadness': 'sad',
    'Angry': 'angry', 'Disgust': 'disgust', 'Fear': 'fear',
    'Happy': 'happy', 'Sad': 'sad', 'Surprise': 'surprise',
    'Neutral': 'neutral'
}

def normalize_label(label):
    return LABEL_MAPPING.get(label, label).lower()

def load_data(data_dir):
    try:
        split = "test" if os.path.exists(os.path.join(data_dir, "test")) else "train"
        dataset = load_dataset("imagefolder", data_dir=data_dir, split=split)
        if split == "train":
            dataset = dataset.train_test_split(test_size=0.2)['test']
        return dataset
    except Exception as e:
        print(f"Error loading {data_dir}: {e}")
        return None

def get_predictions(model_name, repo_id, dataset):
    print(f"Running inference for {model_name}...")
    try:
        processor = ViTImageProcessor.from_pretrained(repo_id)
        model = ViTForImageClassification.from_pretrained(repo_id)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        model.eval()

        y_true = []
        y_score = []

        for item in tqdm(dataset, desc=model_name):
            image = item['image'].convert("RGB")
            true_label_name = dataset.features['label'].int2str(item['label'])
            norm_label = normalize_label(true_label_name)
            
            if norm_label not in LABELS:
                continue
                
            true_idx = LABELS.index(norm_label)
            
            inputs = processor(images=image, return_tensors="pt").to(device)
            with torch.no_grad():
                outputs = model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().numpy()[0]
            
            y_true.append(true_idx)
            y_score.append(probabilities)
            
        return np.array(y_true), np.array(y_score)
    except Exception as e:
        print(f"Error evaluating {model_name}: {e}")
        return None, None

def plot_roc(y_true, y_score, model_name, dataset_name):
    y_true_bin = label_binarize(y_true, classes=range(N_CLASSES))
    
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i in range(N_CLASSES):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Micro-average ROC curve
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    plt.figure(figsize=(10, 8))
    plt.plot(fpr["micro"], tpr["micro"],
             label=f'micro-average ROC (area = {roc_auc["micro"]:0.2f})',
             color='deeppink', linestyle=':', linewidth=4)

    colors = sns.color_palette("husl", N_CLASSES)
    for i, color in zip(range(N_CLASSES), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label=f'ROC {LABELS[i]} (area = {roc_auc[i]:0.2f})')

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC - {model_name} on {dataset_name}')
    plt.legend(loc="lower right")
    
    filename = f"results/roc_{model_name.replace(' ', '_').replace('(', '').replace(')', '')}_{dataset_name}.png"
    plt.savefig(filename)
    plt.close()
    
    return roc_auc["micro"]

def main():
    os.makedirs("results", exist_ok=True)
    summary_auc = []

    for ds_name, ds_path in DATASETS.items():
        dataset = load_data(ds_path)
        if not dataset: continue
        
        for model_name, repo_id in MODELS.items():
            y_true, y_score = get_predictions(model_name, repo_id, dataset)
            if y_true is not None:
                micro_auc = plot_roc(y_true, y_score, model_name, ds_name)
                summary_auc.append({
                    "Model": model_name,
                    "Dataset": ds_name,
                    "Micro AUC": micro_auc
                })

    # Save AUC Summary
    import pandas as pd
    df = pd.DataFrame(summary_auc)
    print("\n--- AUC Summary ---")
    print(df.to_markdown(index=False))
    df.to_csv("results/auc_summary.csv", index=False)

if __name__ == "__main__":
    main()
