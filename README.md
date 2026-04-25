# Project-AEGIS

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0.88-green)](https://docs.opencv.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-orange)](https://docs.ultralytics.com/)

Project-AEGIS is a near-miss risk estimation system for pedestrian-vehicle interactions. It analyzes traffic video, detects people and vehicles, tracks motion over time, computes time-to-collision and relative velocity, and flags potential near-miss events.

## Why it matters

- Detects and scores risky pedestrian-vehicle interactions in video footage
- Supports safety research, urban mobility analysis, and prototype hazard detection
- Provides both a desktop demo pipeline and a FastAPI video analysis service
- Generates visual risk plots and stores incidents for later review

## Getting started

### Prerequisites

- Python 3.8 or higher
- A video file such as MP4, AVI, or MOV
- `yolov8n.pt` model weights committed in the repository

### Install dependencies

```bash
git clone <repository-url>
cd Project-AEGIS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### Verify the environment

```bash
python verify_install.py
```

### Run the desktop demo

1. Put a video under `data/videos/` or change the path in `main.py`
2. Start the demo:

```bash
python main.py
```

3. Press `q` to quit
4. The demo shows bounding boxes, tracked IDs, risk annotations, and saves plots to `data/outputs/`

### Run the API service

Create a `.env` file in the repository root with:

```env
DATABASE_URL=sqlite:///./backend.db
GEMINI_API_KEY=your_gemini_api_key
```

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

Upload a video with a `POST` request to:

```text
http://127.0.0.1:8000/analyze
```

Use a multipart form field named `file`.

## What the project includes

- `main.py` — desktop video processing demo
- `backend/main.py` — FastAPI app with analysis and incident endpoints
- `backend/services/aegis_service.py` — video analysis pipeline for uploads
- `src/detection.py` — YOLOv8 object detection for people and vehicles
- `src/tracking.py` — centroid-based ID tracking
- `src/motion.py` — ground-plane projection, distance, velocity, and TTC
- `src/risk_model.py` — NMRS scoring and near-miss event detection
- `src/visualization.py` — risk signal logging and plot generation
- `verify_install.py` — package install checks
- `test_nmr.py` — environment import smoke test

## API endpoints

- `GET /` — service health check
- `POST /analyze` — upload a video for analysis
- `GET /incidents` — fetch stored incidents
- `GET /stats` — count incidents by risk level
- `GET /videos` — list analyzed videos
- `GET /video/{video_id}` — incident details for a specific analyzed video

## Project layout

```
Project-AEGIS/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── db/
│   │   ├── base.py
│   │   ├── incident.py
│   │   └── session.py
│   └── services/
│       ├── aegis_service.py
│       └── ai_summary.py
├── data/
│   └── videos/
├── notebooks/
├── src/
│   ├── detection.py
│   ├── motion.py
│   ├── risk_model.py
│   ├── tracking.py
│   ├── video_io.py
│   └── visualization.py
├── main.py
├── requirements.txt
├── verify_install.py
├── test_nmr.py
├── yolov8n.pt
└── temp_uploads/
```

## Notes

- The desktop demo is designed for offline video playback.
- The API saves incident data to a SQL database defined by `DATABASE_URL`.
- AI summaries use Gemini via `google-generativeai` if `GEMINI_API_KEY` is configured.

## Getting help

- Inspect `backend/main.py` and `backend/services/aegis_service.py` for service behavior
- Run `verify_install.py` to confirm required packages
- Open a repository issue for bugs or feature requests

## Contributing

1. Fork the repository
2. Create a branch for your feature or fix
3. Add or update tests when possible
4. Submit a pull request

> This repository is intended for research and prototyping. Production use requires additional validation and deployment hardening.
