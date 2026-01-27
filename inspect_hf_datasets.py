from datasets import load_dataset

def inspect_dataset(dataset_name):
    print(f"Inspecting {dataset_name}...")
    try:
        ds = load_dataset(dataset_name, split="train", streaming=True)
        print("Features:", ds.features)
        sample = next(iter(ds))
        print("Sample:", sample)
        if 'label' in sample:
            print("Label:", sample['label'])
    except Exception as e:
        print(f"Error: {e}")

print("--- RAF-DB ---")
inspect_dataset("deanngkl/raf-db-7emotions")

print("\n--- AffectNet ---")
inspect_dataset("deanngkl/affectnet_no_contempt")
