import json      # Standard library for parsing and processing JSON data files.
import sys       # System library to manage system-level operations like script arguments.
import argparse  # Module for building a professional and flexible command line interface.
from router import SmartFilter  # Import the SmartFilter (Small Neuron) from our routing module.

def validate(filename):
    """
    The Validation Engine with high verbosity. 
    It communicates every single step of the 'guessing game' to the user.
    """
    print(f"\n[STEP 1] Starting validation session for: {filename}")
    print(f"--- Accessing file system to load data...")
    
    try:
        # Attempt to open the target JSON file.
        with open(filename, "r") as f:
            dataset = json.load(f)  # Convert the file content into a Python list of dictionaries.
        print(f"--- Data loaded successfully. Detected {len(dataset)} entries to process.")
    except FileNotFoundError:
        # Inform the user if the specified file path is incorrect.
        print(f"!!! Error: File '{filename}' was not found. Please check the path.")
        return
    except json.JSONDecodeError:
        # Catch syntax errors in the JSON file (like a missing comma or bracket).
        print(f"!!! Error: JSON syntax is broken in '{filename}'. Validation aborted.")
        return

    # If the list is empty, there is nothing for the Brain to classify.
    if not dataset:
        print(f"--- Warning: '{filename}' contains no data. Nothing to do.")
        return
        
    print(f"\n[STEP 2] Wake-up sequence: Initializing SmartFilter neuron...")
    smart_filter = SmartFilter()  # Create an active instance of our rule-based router.
    
    success_count = 0             # Track the number of times the router matched the human labels.
    total = len(dataset)          # Keep track of the total number of prompts for percentage calculation.
    results = []                  # Store the logs of every transaction for the final report.
    
    print(f"\n[STEP 3] Beginning the 'Guessing Game' (Neural Routing)...")
    print("=" * 60)

    # Begin iterating through every individual entry in the dataset.
    for i, item in enumerate(dataset):
        # Retrieve the human-written prompt string.
        prompt = item.get("prompt", "")
        item_id = item.get("id", i + 1)
        
        if not prompt:
            # If the entry exists but has no text, skip it to avoid errors.
            print(f"Skipping entry ID {item_id}: No prompt found.")
            continue
            
        print(f"Processing Prompt #{item_id}: \"{prompt[:60]}...\"")
        
        # ACTIVATE ROUTER: The neuron scans the prompt using its internal regex patterns.
        print(f"  -> Thinking... (Scanning keywords and identifying experts)")
        actual = smart_filter.classify(prompt)
        
        # LOG INFERENCE: Show exactly what the router decided for this prompt.
        print(f"  -> Router Decision: {actual['label'].upper()}")
        print(f"  -> Expert Pathways: {', '.join(actual['categories'])}")
        
        # EXTRACT GROUND TRUTH: Look for the 'answer key' in the user's data.
        expected_cat_str = item.get("category")
        
        # HANDLE INFERENCE-ONLY MODE: If there's no ground truth, we just skip comparison.
        if expected_cat_str is None:
            print(f"  -> Result: Completed (Inference Mode - No ground truth found)")
            results.append({
                "id": item_id,
                "prompt": prompt,
                "actual_cats": list(actual["categories"]),
                "actual_label": actual["label"],
                "success": None  # Indicates this was a test, not an accuracy validation.
            })
            print("-" * 40)
            continue

        # GROUND TRUTH COMPARISON: The 'Guessing Game' comparison logic.
        print(f"  -> Verification: Comparing against ground truth ('{expected_cat_str}')")
        
        # Parse ground truth categories (handling the '+' multi-label notation).
        expected_cats = set([c.strip() for c in expected_cat_str.split("+")])
        
        # Mapping for Ambiguous consistency across datasets.
        if expected_cat_str == "Ambiguous":
             expected_cats = set(["Ambiguous"])

        # The router's final triggered expert pathways.
        actual_cats = set(actual["categories"])
        
        is_success = False  # Assume fail until a match is confirmed.
        label = item.get("label", "single") # Type of task (single expert vs multi expert).
        
        # LOGIC FOR 'MATCHING'
        if label == "edge":
            # Edge match: Both must agree it's an ambiguous/edge case.
            is_success = actual["label"] == "edge"
        elif label == "multi":
            # Multi match: Both must agree it's multi-layered + at least 1 expert expert overlaps.
            is_success = (actual["label"] == "multi") and (len(expected_cats.intersection(actual_cats)) > 0)
        else:
            # Single match: The router's guess overlaps with the human labeling.
            is_success = any(cat in actual_cats for cat in expected_cats)
            
        # Record score.
        if is_success:
            print(f"  -> [MATCH FOUND] System synchronized with human judgment.")
            success_count += 1
        else:
            print(f"  -> [MISMATCH] Systems diverged on this specific routing path.")
            
        # Append detailed data for the JSON result log.
        results.append({
            "id": item_id,
            "prompt": prompt,
            "expected_cat": expected_cat_str,
            "actual_cats": list(actual_cats),
            "expected_label": label,
            "actual_label": actual["label"],
            "success": is_success
        })
        print("-" * 40)
        
    # FINAL ANALYTICS CALCULATION
    print("\n[STEP 4] Finalizing Benchmark Research...")
    
    # Calculate the percentage of 'correct' guesses.
    accuracy = (success_count / total) * 100 if total > 0 else 0
    
    # Check if we were doing verification or just real-time inference.
    has_ground_truth = any(r["success"] is not None for r in results)
    
    print("=" * 60)
    print(f"ANALYSIS COMPLETE FOR: {filename}")
    
    if has_ground_truth:
        # Present the final accuracy score if validation was possible.
        print(f"Overall Accuracy: {accuracy:.2f}%")
        print(f"Correct Routings: {success_count} / {total}")
    else:
        # Case for testing test.json where no answers were provided.
        print(f"Processing Finished: {total} prompts routed through the expert gateway.")
    
    # ARCHIVING RESULTS: Save the full trace to a local JSON file for further review.
    output_name = f"results_{filename}"
    with open(output_name, "w") as f:
        json.dump(results, f, indent=4)
    print(f"--- Full architectural trace saved to: {output_name}")
    print("=" * 60)

if __name__ == "__main__":
    # SETUP COMMAND LINE INTERFACE
    parser = argparse.ArgumentParser(description="FinOps Smart Filter Benchmark Tool")
    # File argument (optional). If not given, we default to our 220-prompt ground truth.
    parser.add_argument("file", nargs="?", default="dataset.json", help="JSON dataset to test (default: dataset.json)")
    args = parser.parse_args()
    
    # Launch validation.
    validate(args.file)
