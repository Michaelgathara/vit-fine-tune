from huggingface_hub import list_datasets

def search_datasets(query):
    print(f"Searching for {query}...")
    datasets = list_datasets(search=query, limit=5)
    for d in datasets:
        print(f"- {d.id} ({d.downloads} downloads)")

print("--- RAF-DB ---")
search_datasets("raf-db")

print("\n--- AffectNet ---")
search_datasets("affectnet")
