# IS PROJ

Minimal README for the project.

## Overview

This repository contains code for training and running models in the `backend` folder. Training scripts, datasets, and saved model artifacts are stored under `backend/` and the repository root.

## Repository layout

- `backend/` — application code and training scripts
  - `main.py` — main entrypoint (inference / app)
  - `training/train_model.py` — training script
  - `dataset/` — datasets (may be large)
- `saved_models/` — (model artifacts, ignored by default)
- `requirments.txt` — Python dependencies

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows CMD
venv\Scripts\activate.bat
```

2. Install dependencies:

```bash
pip install -r requirments.txt
```

## Common tasks

- Train model:

```bash
python backend/training/train_model.py
```

- Run the app / inference:

```bash
python backend/main.py
```

## Notes

- Large files (models and datasets) are excluded via `.gitignore`.
- Update this README with usage examples, model format, and dataset instructions as the project evolves.
