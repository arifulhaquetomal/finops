import json
import os
from collections import Counter

dataset_path = '/home/tomal/scratch/finops/dataset/complete_llm_dataset.json'

def clean_prompt(prompt):
    if not isinstance(prompt, str):
        return prompt
    
    # 1. Replace newlines (actual and escaped) with single space
    prompt = prompt.replace('\n', ' ').replace('\\n', ' ')
    
    # 2. Handle unnecessary slashes
    # Note: User mentioned "/" specifically. We'll be cautious not to remove 
    # legitimate slashes (like in "and/or" or dates) but the request sounds like 
    # they want to clean up artifacts.
    # For now, let's remove any stray backslashes which are often artifacts.
    prompt = prompt.replace('\\', '')
    
    # 3. Clean up extra spaces
    prompt = ' '.join(prompt.split())
    
    return prompt

def analyze_dataset(data):
    categories = Counter()
    subcategories = Counter()
    labels = Counter()
    
    for item in data:
        categories[item.get('category', 'Unknown')] += 1
        subcategories[item.get('subcategory', 'Unknown')] += 1
        labels[item.get('label', 'Unknown')] += 1
        
    return categories, subcategories, labels

def main():
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found.")
        return

    with open(dataset_path, 'r') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries.")

    # Clean the prompts
    for item in data:
        item['prompt'] = clean_prompt(item['prompt'])

    # Save cleaned data
    with open(dataset_path, 'w') as f:
        json.dump(data, f, indent=4)
    print("Cleaned dataset saved.")

    # Analyze
    cats, subcats, labs = analyze_dataset(data)

    print("\n--- Categories ---")
    for k, v in cats.items():
        print(f"{k}: {v}")

    print("\n--- Subcategories ---")
    # Subcategories can be many, maybe show top 20 or all?
    # Let's show all since it's an overview.
    for k, v in sorted(subcats.items()):
        print(f"{k}: {v}")

    print("\n--- Labels ---")
    for k, v in labs.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
