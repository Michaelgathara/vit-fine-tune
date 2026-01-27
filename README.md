# Vision Transformer (ViT) Fine-Tuning for Emotion Recognition

This project implements a comprehensive pipeline for fine-tuning Vision Transformer (ViT) models on various facial emotion recognition datasets. It includes tools for data acquisition, preprocessing, training, and evaluation across multiple domains.

## Overview

The system focuses on fine-tuning the `trpakov/vit-face-expression` base model on four distinct datasets and a combined "Universal" dataset to improve robustness and generalization.

### Supported Datasets
1. **Zenodo (IFEED)**: A specialized dataset for emotion recognition.
2. **Mendeley (GFFD-2025)**: Contains both genuine and acted facial expressions.
3. **RAF-DB**: Real-world Affective Faces Database, providing "in-the-wild" images.
4. **AffectNet**: A large-scale database of facial expressions.
5. **Universal**: A combination of all the above for maximum robustness.

## Project Structure

- `data/`: Directory for storing raw and processed datasets (ignored by git).
- `models/`: Directory for saving trained model checkpoints (ignored by git).
- `results/`: Output directory for evaluation metrics and confusion matrices (ignored by git).
- `train.py`: Main training script using Hugging Face Trainer.
- `evaluate_all_v2.py`: Comprehensive evaluation script generating comparison reports.
- `setup_data.py`: Script to download Zenodo dataset.
- `prepare_zenodo.py`: Preprocessing script for Zenodo data.
- `prepare_mendeley.py`: Preprocessing script for Mendeley data.
- `prepare_hf_datasets.py`: Script to download and prepare RAF-DB and AffectNet.
- `prepare_combined_dataset.py`: Script to merge all datasets into the Universal set.
- `test_inference.py`: Simple script to test model inference on a single image.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Prepare Datasets:
   Run the various preparation scripts to download and format the data into `data/`.

3. Training:
   Use `train.py` to fine-tune a model. Example:
   ```bash
   python train.py --data_dir data/zenodo_processed --output_dir models/zenodo_finetuned --epochs 3 --batch_size 8
   ```

4. Evaluation:
   Run the evaluation suite to compare models:
   ```bash
   python evaluate_all_v2.py
   ```

## Models

The following fine-tuned models have been produced and are available on Hugging Face:

- [`michaelgathara/vit-face-zenodo`](https://huggingface.co/michaelgathara/vit-face-zenodo)
- [`michaelgathara/vit-face-mendeley`](https://huggingface.co/michaelgathara/vit-face-mendeley)
- [`michaelgathara/vit-face-raf-db`](https://huggingface.co/michaelgathara/vit-face-raf-db)
- [`michaelgathara/vit-face-affectnet`](https://huggingface.co/michaelgathara/vit-face-affectnet)
- [`michaelgathara/vit-face-universal`](https://huggingface.co/michaelgathara/vit-face-universal)

## Results

Detailed evaluation results, including accuracy metrics and confusion matrices for each model-dataset pair, can be generated using the evaluation script. The "Universal" model demonstrates the best overall generalization across different domains.
