# AI-Based Intelligent Traffic Safety System

An Event-Driven AI Engine for detecting traffic violations, emergency vehicles, and road hazards.

## Features
- **Wrong-Side Driving Detection**: Tracks vehicle vectors to identify lane violations.
- **Emergency Vehicle Priority**: Identifies ambulances/fire trucks and triggers priority events.
- **Pothole Detection**: Tags road hazards with severity levels.
- **Event-Driven Architecture**: Decoupled Detection, Rules, and Actions using an internal Event Bus.
- **Dashboard**: Real-time Streamlit visualization of events.

## Installation

1.  **Clone/Download** the repository.
2.  **Set up Virtual Environment (Recommended)**:
    ```bash
    # Create venv
    python -m venv venv

    # Activate (Windows)
    .\venv\Scripts\activate
    ```

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
