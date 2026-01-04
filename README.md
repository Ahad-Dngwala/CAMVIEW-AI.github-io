<div align="center">

# 🛣️ CAMVIEW.AI
### Enterprise-Grade Intelligent Traffic Safety Intelligence System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.32-FF4B4B.svg)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv11-green)](https://docs.ultralytics.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img width="1919" height="1079" alt="Screenshot 2026-01-04 234631" src="https://github.com/user-attachments/assets/54765446-c881-478e-becd-47f7e041eee4" /><img width="1919" height="1079" alt="Screenshot 2026-01-04 234712" src="https://github.com/user-attachments/assets/31723fe5-758a-44fc-97ba-f2f8e6953b2a" />
<img width="1919" height="1078" alt="Screenshot 2026-01-04 234732" src="https://github.com/user-attachments/assets/3b5de38e-2eee-464a-9661-80db4a1ef5bf" />
<img width="1917" height="1079" alt="Screenshot 2026-01-04 234746" src="https://github.com/user-attachments/assets/129f33d8-ae88-4eb8-80ee-a8826f6237b8" />
<img width="1919" height="1079" alt="Screenshot 2026-01-04 234820" src="https://github.com/user-attachments/assets/efd31341-835b-4e2d-8fe3-26b70db8a1bd" />


**Beyond Simple Detection: Real-Time Event Reasoning for Safer Roads**

[Features](#-core-features) • [Architecture](#-system-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Dashboard](#-real-time-dashboard)

</div>

---

## 🔍 The Problem

Modern traffic monitoring systems face significant challenges:
- ❌ **High False Positives**: Traditional single-frame detection triggers incorrectly on shadows or static objects.
- ❌ **Delayed Response**: Manual surveillance cannot react instantly to critical hazards.
- ❌ **Fragmented Data**: Disconnected systems for violations, emergencies, and maintenance (potholes) create data silos.
- ❌ **Lack of Context**: Simple object detection fails to understand *behavior* over time (e.g., wrong-way driving).

## 💡 The CAMVIEW.AI Solution

**CAMVIEW.AI** moves beyond basic object detection. It is an **Event-Driven Computer Vision System** that transforms raw video feeds into structured, actionable safety intelligence.

By combining deep learning with temporal logic and an event bus architecture, it reasons about motion, context, and persistence to deliver **enterprise-grade reliability**.

---

## ✨ Core Features

### 🚘 **Wrong-Side Driving Detection**
- **Temporal Tracking**: Tracks vehicle motion vectors across multiple frames, not just single images.
- **Lane-Aware Logic**: Uses directional smoothing to confirm violations only after consistent behavior.
- **False-Positive Suppression**: Eliminates duplicate alerts for the same vehicle.

### 🚑 **Emergency Vehicle Priority**
- **Visual Recognition**: Detects ambulances, fire trucks, and police vehicles using vision cues.
- **Preemption Ready**: Generates high-priority events designed for integration with smart traffic signals.
- **Priority Logging**: Flags events for immediate attention in the dashboard.

### 🕳️ **Pothole Detection & Analytics**
- **Hazard Identification**: Detects road surface irregularities in real-time.
- **Severity Estimation**: Automatically assigns severity (Low/Medium/High) based on hazard size/area.
- **Maintenance Data**: Provides structured logs for infrastructure planning.

### 🧠 **Event-Driven Architecture (Key Differentiator)**
- **Decoupled Design**: Separates Detection, Rules, and Actions.
- **Internal Event Bus**: Events flow asynchronously through the system.
- **Extensible**: Add new detectors (e.g., helmet detection) without rewriting the logging or UI code.

---

## 🏗️ System Architecture

<img width="2638" height="1371" alt="Mind Map" src="https://github.com/user-attachments/assets/8cab1bfe-a78e-4653-9a74-a288f69d6291" />


```mermaid
graph TD
    A[Video Source] -->|Frames| B(Unified Processor)
    B -->|Inference| C{YOLO Detectors}
    C -->|Detections| D[Context & Rules Engine]
    D -->|Valid Events| E[Event Bus]
    E -->|Publish| F[JSONL Logger]
    E -->|Publish| G[Firebase Cloud]
    E -->|Publish| H[Console Alert]
    
    subgraph Dashboard[Streamlit Enterprise Dashboard]
        I[Real-Time Monitor]
        J[Analytics Engine]
        K[Data Export]
    end
    
    F -->|Read| Dashboard
    G -->|Sync| Dashboard
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Core Logic** | Python 3.10+ | Engine & Event Bus implementation |
| **Vision** | OpenCV | Video capture using hardware acceleration |
| **AI Model** | Ultralytics YOLO | Object Detection, Classification & Tracking |
| **UI/UX** | Streamlit | Real-time Enterprise Dashboard |
| **Cloud** | Firebase | Cloud syncing & Remote Monitoring (Optional) |
| **Logging** | JSONL | High-performance, append-only structured logs |
| **Data** | Pandas & Plotly | Advanced Analytics & Interactive Visualizations |

---

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/CAMVIEW.AI.git
    cd CAMVIEW.AI
    ```

2.  **Create Virtual Environment (Recommended)**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    > *Note: First run will automatically download necessary YOLO models.*

---

## ▶️ Usage

### 1. Run the AI Engine
Start the backend detection engine. This processes video and generates events.
```bash
# Use Webcam
python main.py --source 0

# Use Video File
python main.py --source data/raw/traffic_video.mp4
```

### 2. Launch the Dashboard
Open a new terminal to run the visualization interface.
```bash
streamlit run app.py
```
> Access the dashboard at **http://localhost:8501**

---

## 📊 Real-Time Dashboard

The system includes a **Streamlit-based Enterprise Dashboard**:
*   **Live Preview**: Low-latency video feed with bounding box overlays.
*   **Event Feed**: Real-time scrolling log of violations and hazards.
*   **Analytics Tab**: Interactive charts for Event Type Distribution, Severity Timeline, and Hourly Heatmaps.
*   **Data Export**: Download logs in CSV, JSON, or Excel formats.

---

## ⚠️ Limitations & Integrity

We believe in honest engineering. Current system constraints:
*   **Streamlit FPS**: Optimized for stability over raw speed (approx 5-10 FPS preview).
*   **Geo-Tagging**: Pothole locations are currently relative to the frame, not GPS coordinates.
*   **Lighting**: Performance may decrease in extreme low-light conditions without IR cameras.

---

## 🚀 Future Roadmap

- [ ] **GPS Integration**: Google Maps API for real-world pothole plotting.
- [ ] **RTSP Support**: Native integration for IP Security Cameras.
- [ ] **WebRTC**: Lower latency video streaming for the dashboard.
- [ ] **Edge Deployment**: Optimization for Jetson Nano / Raspberry Pi 5.

---

<div align="center">

**© 2026 CAMVIEW.AI** • *Engineering Safety Intelligence*

</div>


3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    (Note: `ultralytics` will automatically download the YOLOv8 model on first run).

## Usage

### 1. Run the AI Engine (Terminal)
This runs the main detection loop and prints alerts to the console.
```bash
# Run with webcam
python main.py --source 0

# Run with a video file
python main.py --source data/raw/traffic_video.mp4
```

### 2. Run the Dashboard
Open a separate terminal to view the live dashboard.
```bash
streamlit run app.py
```

## Folder Structure
- `core/`: Core engine, Event Bus, and Event definitions.
- `detectors/`: Specific logic for each problem statement (Wrong-side, etc.).
- `config/`: Settings and constants.
- `data/logs/`: Stores `events.jsonl` for the dashboard.
