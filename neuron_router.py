import joblib
import os
import re

class NeuronRouter:
    """
    A Local Neuron Router using a trained Machine Learning model.
    """
    def __init__(self, model_path="neuron_model.pkl", vectorizer_path="vectorizer.pkl", mlb_path="mlb.pkl"):
        # Load the artifacts
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = joblib.load(os.path.join(current_dir, model_path))
        self.vectorizer = joblib.load(os.path.join(current_dir, vectorizer_path))
        self.mlb = joblib.load(os.path.join(current_dir, mlb_path))

    def classify(self, text):
        # Transform the text
        X = self.vectorizer.transform([text])
        
        # Predict categories
        y_pred = self.model.predict(X)
        
        # Convert binary matrix back to category labels
        categories = self.mlb.inverse_transform(y_pred)[0]
        
        # If no categories triggered, return Ambiguous
        if not categories:
            return {
                "categories": ["Ambiguous"],
                "label": "edge"
            }
        
        return {
            "categories": list(categories),
            "label": "single" if len(categories) == 1 else "multi"
        }

if __name__ == "__main__":
    # Test block
    router = NeuronRouter()
    print(router.classify("Write a python function to sort a list"))
    print(router.classify("What is the capital of France?"))
    print(router.classify("Help"))
