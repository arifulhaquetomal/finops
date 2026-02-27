import json      # Standard library for parsing JSON data files.
import sys       # System library to handle potential exit codes or arguments.
import argparse  # Module for creating a professional command-line interface.
import os        # Module for interacting with the operating system.
from router import SmartFilter  # Importing our classifier
from neuron_router import NeuronRouter # Importing our ML neuron

def validate(filename, router_type="regex"):
    """
    The main validation engine. It compares the router's 'guesses' 
    against the professional ground truth data.
    """
    try:
        # Open the specified file (either the reference or a test file).
        with open(filename, "r") as f:
            dataset = json.load(f)  # Load the entire list of prompts into memory.
    except FileNotFoundError:
        # Safety check: if the user types a filenames that doesn't exist.
        print(f"Error: {filename} not found.")
        return
    except json.JSONDecodeError:
        # Safety check: if the JSON syntax is broken (missing comma, etc).
        print(f"Error: {filename} is not a valid JSON file.")
        return

    # If the file is just '[]', there's nothing for us to classify.
    if not dataset:
        print(f"File {filename} is empty. No prompts to test.")
        return
        
    print(f"--- INITIALIZING {router_type.upper()} ROUTER ---")
    if router_type == "neuron":
        smart_filter = NeuronRouter()
    else:
        smart_filter = SmartFilter()

    success_count = 0             # Counter for 'correct guesses' against ground truth.
    total = len(dataset)          # Total number of items we need to process.
    
    results = []  # List to store the detailed log of every single test run.
    
    verbose = getattr(args, 'verbose', False)
    
    # START OF THE "GUESSING GAME" LOOP
    for i, item in enumerate(dataset):
        # Extract the human prompt from the JSON object.
        prompt = item.get("prompt", "")
        if not prompt:
            # If a JSON entry is missing a 'prompt' key, skip it.
            continue
            
        # STEP 1: MAKE A GUESS. Pass the prompt to the SmartFilter.
        actual = smart_filter.classify(prompt)
        
        # STEP 2: FIND THE ANSWER KEY.
        expected_cat_str = item.get("category", "Ambiguous")
        expected_cats = set([c.strip() for c in expected_cat_str.split("+")])
        
        # Special mapping for the 'Ambiguous' pathway.
        if expected_cat_str == "Ambiguous":
             expected_cats = set(["Ambiguous"])

        # The actual experts the router triggered.
        actual_cats = set(actual["categories"])
        is_success = False  
        
        # Determine success based on the manual labels in the Answer Key.
        label = item.get("label", "single")
        if label == "edge":
            is_success = actual["label"] == "edge"
        elif label == "multi":
            is_success = (actual["label"] == "multi") and (len(expected_cats.intersection(actual_cats)) > 0)
        else:
            is_success = any(cat in actual_cats for cat in expected_cats)
            
        if is_success:
            success_count += 1
            
        # Log the result of this specific "Guess".
        if verbose:
            print(f"ID {item.get('id', '?')}: {'CORRECT' if is_success else 'WRONG'} (Goal: {expected_cat_str} | Router Guess: {', '.join(actual_cats)})")
        elif (i + 1) % 50 == 0 or (i + 1) == total:
            print(f"Progress: {i+1}/{total} items processed...")
            
        # Log entry for results file.
        results.append({
            "id": item.get("id"),
            "prompt": prompt,
            "expected_cat": expected_cat_str,
            "actual_cats": list(actual_cats),
            "expected_label": label,
            "actual_label": actual["label"],
            "success": is_success
        })
        
    # FINAL BENCHMARK CALCULATION
    accuracy = (success_count / total) * 100 if total > 0 else 0
    print(f"\nFinal Statistics for {filename}:")
    print(f"Benchmark Score: {accuracy:.2f}% ({success_count}/{total} correct guesses)")
    
    # Save results to disk in a dedicated 'results' folder.
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    sanitized_filename = filename.replace("/", "_").replace("\\", "_")
    output_name = os.path.join(results_dir, f"results_{sanitized_filename}")
    with open(output_name, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Detailed performance logs saved to {output_name}")

if __name__ == "__main__":
    # COMMAND LINE INTERFACE SETUP
    parser = argparse.ArgumentParser(description="Validate the Smart Filter.")
    # Add an optional argument for the filename.
    # Default: dataset.json (the reference ground truth).
    parser.add_argument("file", nargs="?", default="dataset.json", help="JSON file to validate (default: dataset.json)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed results for every prompt")
    parser.add_argument("--mode", "-m", choices=["regex", "neuron"], default="regex", help="Routing mode: regex or neuron (default: regex)")
    args = parser.parse_args()
    
    # Execute the validation engine.
    validate(args.file, router_type=args.mode)
