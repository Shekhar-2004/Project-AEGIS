# Project-AEGIS: Near-Miss Risk Estimation System

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0.88-green.svg)](https://opencv.org/)
[![Ultralytics](https://img.shields.io/badge/Ultralytics-YOLOv8-orange.svg)](https://ultralytics.com/)

A real-time computer vision system for detecting and analyzing near-miss events between pedestrians and vehicles using advanced object detection, tracking, and risk modeling algorithms.

## What the Project Does

Project-AEGIS processes video streams to identify potential safety hazards by:

- **Object Detection**: Uses YOLOv8 to detect people and vehicles in real-time
- **Object Tracking**: Maintains consistent tracking of detected objects across frames
- **Motion Analysis**: Calculates relative motion parameters between tracked objects
- **Risk Assessment**: Computes Near-Miss Risk Scores (NMRS) based on distance, time-to-collision, and velocity
- **Event Detection**: Identifies near-miss events using temporal smoothing and threshold-based detection
- **Visualization**: Provides real-time visual feedback with bounding boxes and risk indicators
- **Logging**: Records risk signals for post-analysis and generates performance plots

## Why the Project is Useful

This system addresses critical safety challenges in transportation and urban environments by:

- **Proactive Safety**: Detects potential collisions before they occur
- **Data-Driven Insights**: Provides quantitative risk metrics for safety analysis
- **Real-time Monitoring**: Enables immediate response to developing hazards
- **Research Applications**: Supports studies in traffic safety, pedestrian behavior, and risk modeling
- **Infrastructure Planning**: Helps identify high-risk zones and optimize safety measures

## How Users Can Get Started

### Prerequisites

- Python 3.8 or higher
- Video file for processing (MP4 format recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Minor_Project
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv nmrs_env
   # On Windows:
   nmrs_env\Scripts\activate
   # On macOS/Linux:
   source nmrs_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python verify_install.py
   ```

### Usage

1. **Prepare video data**
   Place your video file in the `data/videos/` directory (e.g., `test_near_miss.mp4`)

2. **Run the system**
   ```bash
   python main.py
   ```

3. **View results**
   - Real-time video processing with bounding boxes and risk indicators
   - Press 'q' to quit
   - Risk signals are automatically logged and plotted after processing

### Configuration

The system uses default YOLOv8 nano model (`yolov8n.pt`). For custom models:
- Replace `yolov8n.pt` with your trained model
- Adjust confidence threshold in `ObjectDetector` class if needed

## Project Structure

```
Minor_Project/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── verify_install.py       # Installation verification script
├── test_nmr.py            # Basic functionality tests
├── yolov8n.pt             # YOLOv8 nano model weights
├── data/
│   ├── videos/            # Input video files
│   └── outputs/           # Generated outputs and logs
├── src/                   # Core modules
│   ├── detection.py       # YOLO-based object detection
│   ├── tracking.py        # Centroid-based object tracking
│   ├── motion.py          # Relative motion analysis
│   ├── risk_model.py      # NMRS computation and event detection
│   ├── visualization.py   # Signal logging and plotting
│   └── video_io.py        # Video input/output utilities
├── notebooks/             # Jupyter notebooks for analysis
└── nmrs_env/              # Virtual environment (created during setup)
```

## Key Components

### Object Detection (`detection.py`)
- Utilizes Ultralytics YOLOv8 for real-time object detection
- Filters detections for persons and vehicles (car, bus, truck, motorcycle)
- Configurable confidence thresholds

### Tracking (`tracking.py`)
- Centroid-based tracking algorithm
- Maintains object identities across frames
- Handles object entry/exit from frame

### Motion Analysis (`motion.py`)
- Calculates relative distances between tracked objects
- Computes time-to-collision (TTC) estimates
- Tracks velocity vectors for risk assessment

### Risk Modeling (`risk_model.py`)
- Implements Near-Miss Risk Score (NMRS) computation
- Uses distance, TTC, and relative velocity for risk quantification
- Applies temporal smoothing for stable risk signals

### Event Detection (`risk_model.py`)
- Threshold-based near-miss event detection
- Temporal smoothing to reduce false positives
- Maintains event history for analysis

### Visualization (`visualization.py`)
- Real-time video overlay with bounding boxes
- Risk score display and near-miss alerts
- Signal logging and matplotlib-based plotting

## Where Users Can Get Help

### Documentation
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyTorch Documentation](https://pytorch.org/docs/)

### Support
- Create an issue in the repository for bug reports or feature requests
- Check existing issues for common problems and solutions

### Troubleshooting
- Ensure all dependencies are installed correctly using `verify_install.py`
- Verify video file format and path in `main.py`
- Check Python version compatibility (3.8+ required)

## Who Maintains and Contributes

### Maintainers
This project is maintained by the development team as part of a minor project initiative.

### Contributing
We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This system is designed for research and educational purposes. For production safety-critical applications, additional validation and testing should be performed.
