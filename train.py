import argparse
import os
import torch
from datasets import load_dataset
from transformers import ViTImageProcessor, ViTForImageClassification, TrainingArguments, Trainer
from torchvision.transforms import (
    Compose,
    Resize,
    ToTensor,
    Normalize,
    RandomHorizontalFlip,
    RandomRotation,
    ColorJitter
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    args = parser.parse_args()

    model_name = "trpakov/vit-face-expression"
    processor = ViTImageProcessor.from_pretrained(model_name)
    
    # Check for train/test split structure
    data_files = {}
    if os.path.exists(os.path.join(args.data_dir, "train")):
        dataset = load_dataset("imagefolder", data_dir=args.data_dir)
    else:
        # Auto split if flat directory
        dataset = load_dataset("imagefolder", data_dir=args.data_dir)
        dataset = dataset['train'].train_test_split(test_size=0.2)

    labels = dataset['train'].features['label'].names
    label2id = {label: str(i) for i, label in enumerate(labels)}
    id2label = {str(i): label for i, label in enumerate(labels)}

    print(f"Labels: {labels}")

    size = (processor.size["height"], processor.size["width"])
    normalize = Normalize(mean=processor.image_mean, std=processor.image_std)

    train_transforms = Compose([
        Resize(size),
        RandomHorizontalFlip(),
        RandomRotation(10),
        ColorJitter(brightness=0.1, contrast=0.1),
        ToTensor(),
        normalize,
    ])

    val_transforms = Compose([
        Resize(size),
        ToTensor(),
        normalize,
    ])

    def preprocess_train(example_batch):
        example_batch["pixel_values"] = [
            train_transforms(image.convert("RGB")) for image in example_batch["image"]
        ]
        return example_batch

    def preprocess_val(example_batch):
        example_batch["pixel_values"] = [
            val_transforms(image.convert("RGB")) for image in example_batch["image"]
        ]
        return example_batch

    train_ds = dataset['train']
    if 'test' in dataset:
        val_ds = dataset['test']
    elif 'validation' in dataset:
        val_ds = dataset['validation']
    else:
        print("No validation/test split found. Splitting train dataset...")
        splits = train_ds.train_test_split(test_size=0.2)
        train_ds = splits['train']
        val_ds = splits['test']

    train_ds.set_transform(preprocess_train)
    val_ds.set_transform(preprocess_val)

    model = ViTForImageClassification.from_pretrained(
        model_name,
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True
    )

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_dir=f"{args.output_dir}/logs",
        logging_steps=10,
        learning_rate=args.learning_rate,
        num_train_epochs=args.epochs,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        push_to_hub=False,
        remove_unused_columns=False, 
    )

    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = predictions.argmax(axis=1)
        return {"accuracy": (predictions == labels).mean()}

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=processor,
        compute_metrics=compute_metrics,
        data_collator=lambda x: {
            "pixel_values": torch.stack([item["pixel_values"] for item in x]),
            "labels": torch.tensor([item["label"] for item in x])
        }
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    processor.save_pretrained(args.output_dir)

if __name__ == "__main__":
    main()
