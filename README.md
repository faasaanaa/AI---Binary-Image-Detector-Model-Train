# IS PROJ

## Overview

This repository contains the Python backend and a minimal dark themed Next.js frontend.

- `backend/` holds the model training and inference code.
- `front end/` holds the Next.js app for image upload, processing, and result display.

## Repository layout

- `backend/` — application code and training scripts
  - `main.py` — main entrypoint (inference / app)
  - `training/train_model.py` — training script
  - `dataset/` — datasets (may be large)
- `saved_models/` — (model artifacts, ignored by default)
- `front end/` — Next.js frontend app
- `requirments.txt` — Python dependencies

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
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

- Run the frontend:

```bash
cd "front end"
npm install
npm run dev
```

## Notes

- Large files (models, datasets, and Next build output) are excluded via `.gitignore`.
- Update this README with API wiring details when the frontend is connected to the backend model.
