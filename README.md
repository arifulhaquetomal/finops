# FinOps Project: Quick Start Guide

This guide will show you how to run the project from any terminal.

## 1. Navigate to the Project
```bash
cd /home/tomal/scratch/finops
```

## 2. Activate the Environment
Always activate the virtual environment so the scripts have access to `scikit-learn` and `pandas`.
```bash
source venv/bin/activate
```

## 3. Run the Validation (The Benchmark)
The `validate.py` script is the main entry point to see the router in action.

### Run with the Local Neuron (High Accuracy)
Recommended for the best performance (95.76% accuracy).
```bash
python3 validate.py dataset/complete_llm_dataset.json --mode neuron
```

### Run with the Regex Router (Baseline)
To see how the original keyword-based approach compares (55.30% accuracy).
```bash
python3 validate.py dataset/complete_llm_dataset.json --mode regex
```

## 4. Retraining the Neuron (Optional)
If you update the dataset in `dataset/complete_llm_dataset.json`, you can re-teach the neuron by running:
```bash
python3 train_neuron.py
```
This will overwrite the `.pkl` weight files with new knowledge.

## Summary of Files
- **`router.py`**: The original Regex-based logic (optimized).
- **`neuron_router.py`**: The new ML-based logic (The "Neuron").
- **`train_neuron.py`**: The "Teacher" that trains the model.
- **`validate.py`**: The benchmarking tool to test both routers.
