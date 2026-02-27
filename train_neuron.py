import json
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
import os

def train():
    print("--- LOADING DATASET ---")
    with open("dataset/complete_llm_dataset.json", "r") as f:
        data = json.load(f)

    # Prepare data for Multi-Label classification
    texts = []
    labels = []
    
    for item in data:
        prompt = item.get("prompt")
        category_str = item.get("category", "Ambiguous")
        
        if not prompt:
            continue
            
        # Split categories by + and strip whitespace
        cats = [c.strip() for c in category_str.split("+")]
        
        texts.append(prompt)
        labels.append(cats)

    print(f"Loaded {len(texts)} prompts.")

    # Convert labels to binary format for multi-label support
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(labels)
    
    print(f"Categories identified: {mlb.classes_}")

    # Vectorize text using TF-IDF
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        stop_words='english'
    )
    X = vectorizer.fit_transform(texts)

    print("--- TRAINING NEURON (Logistic Regression) ---")
    model = OneVsRestClassifier(LogisticRegression(class_weight='balanced', max_iter=1000))
    model.fit(X, y)

    # Save the artifacts
    print("--- SAVING MODEL ARTIFACTS ---")
    joblib.dump(model, "neuron_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    joblib.dump(mlb, "mlb.pkl")
    print("Training complete. Artifacts saved: neuron_model.pkl, vectorizer.pkl, mlb.pkl")

if __name__ == "__main__":
    train()
