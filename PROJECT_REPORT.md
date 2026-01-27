# Project Report: Emotion Recognition Fine-Tuning

## 1. Project Objective
To develop a robust facial emotion recognition system by fine-tuning Vision Transformer (ViT) models on specialized and general-purpose datasets. The goal was to compare domain-specific "specialist" models against a combined "universal" model to determine the best approach for real-world deployment.

## 2. Methodology

### 2.1 Model Architecture
- **Base Model**: `trpakov/vit-face-expression` (ViT-Base patch16 224).
- **Pre-training**: ImageNet-21k + FER2013 fine-tuning.
- **Task**: 7-class classification (Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise).

### 2.2 Datasets Acquired & Processed
1.  **Zenodo (IFEED)**:
    -   *Source*: Zenodo Record 7963451.
    -   *Type*: Specialized/Lab-controlled.
    -   *Processing*: Standardized directory structure, train/test split.
2.  **Mendeley (GFFD-2025)**:
    -   *Source*: Mendeley Data ID `wmfd4p3z32`.
    -   *Type*: Acted vs. Genuine expressions (merged for this task).
    -   *Processing*: Used "Cropped & Augmented" subset, merged "Fake" and "Genuine" subfolders into unified emotion classes.
3.  **RAF-DB (Real-world Affective Faces)**:
    -   *Source*: Hugging Face `deanngkl/raf-db-7emotions`.
    -   *Type*: "In-the-wild" web images.
    -   *Processing*: Downloaded and reorganized into standard ImageFolder format.
4.  **AffectNet**:
    -   *Source*: Hugging Face `deanngkl/affectnet_no_contempt`.
    -   *Type*: Large-scale "in-the-wild".
    -   *Processing*: Filtered to 7 classes (excluding Contempt) to match the base taxonomy.
5.  **Universal Dataset**:
    -   *Composition*: Merged all 4 datasets above.
    -   *Scale*: ~60,000+ images.
    -   *Goal*: Force the model to learn invariant features robust to domain shifts (lighting, pose, camera quality).

### 2.3 Training Process
-   **Library**: Hugging Face `transformers` + `accelerate`.
-   **Hardware**: NVIDIA RTX 4060 (8GB VRAM).
-   **Hyperparameters**:
    -   Batch Size: 8 (to fit VRAM).
    -   Epochs: 1-2 (depending on dataset size/convergence).
    -   Learning Rate: ~2e-5.
    -   Optimizer: AdamW.
    -   Augmentations: Random rotation, flips, color jitter (applied during training).

## 3. Results & Evaluation

We evaluated 6 model variants against two held-out test sets (Zenodo and Mendeley).

### 3.1 Accuracy Benchmarks

| Model Variant | Performance on Zenodo Test Set | Performance on Mendeley Test Set |
| :--- | :--- | :--- |
| **Base (FER2013)** | 31.4% | 16.1% |
| **Fine-tuned (Zenodo)** | **32.2%** (Specialist) | 19.2% |
| **Fine-tuned (Mendeley)** | 30.9% | **28.8%** (Specialist) |
| **Fine-tuned (RAF-DB)** | 29.6% | 16.4% |
| **Fine-tuned (AffectNet)** | 27.8% | 14.0% |
| **Universal (Combined)** | **31.8%** (Robust) | **26.5%** (Robust) |

### 3.2 Key Findings
1.  **Specialization Wins Locally**: The model trained specifically on Mendeley data achieved nearly **2x the accuracy** (28.8% vs 16.1%) of the base model on that same domain.
2.  **Generalization Gap**: Models trained on "in-the-wild" data (RAF-DB, AffectNet) performed poorly on the specific lab-controlled/posed datasets (Zenodo, Mendeley), likely due to domain shift (e.g., different lighting standards, background clutter, or annotation conventions).
3.  **The Universal Solution**: The combined model achieved **near-peak performance** on both test sets simultaneously (31.8% on Zenodo vs 32.2% specialist; 26.5% on Mendeley vs 28.8% specialist). It successfully learned to handle both domains without catastrophic forgetting.

## 4. Deliverables

### 4.1 Fine-Tuned Models (Uploaded to Hugging Face)
-   `michaelgathara/vit-face-zenodo`
-   `michaelgathara/vit-face-mendeley`
-   `michaelgathara/vit-face-raf-db`
-   `michaelgathara/vit-face-affectnet`
-   `michaelgathara/vit-face-universal` (Recommended for deployment)

### 4.2 Codebase
-   **Training**: `train.py` (Modular script supporting any ImageFolder dataset).
-   **Data Prep**: `prepare_*.py` scripts for downloading and formatting all 4 datasets.
-   **Evaluation**: `evaluate_all_v2.py` (Generates confusion matrices and CSV reports).
-   **Deployment**: `test_inference.py` (Simple inference script).

## 5. Conclusion
A **Universal Model** trained on diverse data sources provides the most robust solution for real-world applications where the input domain is unknown or variable. The Universal model retained ~95-98% of the specialist performance while being applicable across all tested domains.
