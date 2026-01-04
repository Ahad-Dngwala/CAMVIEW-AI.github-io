import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_VIDEO_DIR = os.path.join(DATA_DIR, "raw")
LOG_DIR = os.path.join(DATA_DIR, "logs")
EVENT_LOG_FILE = os.path.join(LOG_DIR, "events.jsonl")

# Detection Config
YOLO_MODEL_PATH = "yolo11n.pt" 
CONFIDENCE_THRESHOLD = 0.5

# Lane boundaries (x‑coordinates). Empty list means auto‑split into two equal lanes.
LANE_BOUNDARIES = []  # e.g. [300, 600] for three‑lane road

WRONG_SIDE_COOLDOWN = 6.0  # Increased cooldown to reduce spam
WRONG_SIDE_MIN_FRAMES = 5  # Require 5 consecutive frames of "wrong way" before multiple alerts
WRONG_SIDE_CONFIDENCE = 0.65 # Higher threshold for violation detection
DIRECTION_SMOOTHING_FRAMES = 5 # Average vector over N frames

POTHOLE_MIN_AREA = 500  # Pixels

# Firebase Configuration
FIREBASE_CREDENTIALS = os.path.join(BASE_DIR, "firebase_service_account.json")
FIREBASE_EVENT_COLLECTION = "traffic_safety_events"

# User Configurable Settings (will be overridden by UI)
USER_EVENT_LOG_FILE = EVENT_LOG_FILE
USER_FIREBASE_CREDENTIALS = FIREBASE_CREDENTIALS

