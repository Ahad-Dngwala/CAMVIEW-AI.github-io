import cv2
import time
import threading
import json
import os
from datetime import datetime
from ultralytics import YOLO
import numpy as np

class RealTimeYOLODetector:
    def __init__(self):
        self.model = YOLO('yolo11n.pt')
        self.cap = None
        self.running = False
        self.events_log = []
        self.frame_count = 0
        self.start_time = time.time()
        
    def start_webcam_detection(self):
        """Start real-time YOLO detection on webcam in separate window"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            return
            
        self.running = True
        print("🔴 Real-time YOLO Detection Started")
        print("Press 'q' to quit, 's' to save screenshot")
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            self.frame_count += 1
            
            # Run YOLO detection
            results = self.model(frame, verbose=False)
            
            # Process detections
            current_time = time.time()
            fps = self.frame_count / (current_time - self.start_time)
            
            # Draw detections on frame
            annotated_frame = results[0].plot()
            
            # Add info overlay
            cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Frame: {self.frame_count}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Detections: {len(results[0].boxes)}", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Log events for traffic safety
            self.log_traffic_events(results[0], current_time)
            
            # Display frame
            cv2.imshow('🔴 Real-Time YOLO Traffic Detection', annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f"detection_screenshot_{timestamp}.jpg", annotated_frame)
                print(f"📸 Screenshot saved: detection_screenshot_{timestamp}.jpg")
        
        self.stop_detection()
    
    def start_video_detection(self, video_path):
        """Start YOLO detection on video file"""
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            return
            
        self.running = True
        print(f"🎬 YOLO Detection Started for: {video_path}")
        print("Press 'q' to quit, 's' to save screenshot")
        
        # Get video info
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Video processing completed")
                break
                
            self.frame_count += 1
            
            # Run YOLO detection
            results = self.model(frame, verbose=False)
            
            # Draw detections on frame
            annotated_frame = results[0].plot()
            
            # Add info overlay
            progress = (self.frame_count / total_frames) * 100
            cv2.putText(annotated_frame, f"Frame: {self.frame_count}/{total_frames}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Progress: {progress:.1f}%", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Detections: {len(results[0].boxes)}", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Log events for traffic safety
            self.log_traffic_events(results[0], time.time())
            
            # Display frame
            cv2.imshow('🎬 YOLO Video Detection', annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f"video_detection_screenshot_{timestamp}.jpg", annotated_frame)
                print(f"📸 Screenshot saved: video_detection_screenshot_{timestamp}.jpg")
        
        self.stop_detection()
    
    def log_traffic_events(self, results, current_time):
        """Log traffic safety events"""
        detections = []
        
        for box in results.boxes:
            if box.conf > 0.5:  # Confidence threshold
                cls = int(box.cls)
                conf = float(box.conf)
                
                # Map YOLO classes to traffic safety events
                traffic_events = {
                    0: 'person',      # pedestrian
                    1: 'bicycle',     # bicycle
                    2: 'car',         # car
                    3: 'motorcycle',  # motorcycle
                    5: 'bus',         # bus
                    7: 'truck',       # truck
                }
                
                if cls in traffic_events:
                    event_type = traffic_events[cls]
                    
                    # Determine severity based on object type and confidence
                    if event_type in ['person', 'bicycle']:
                        severity = 'CRITICAL'
                    elif event_type in ['motorcycle']:
                        severity = 'WARNING'
                    else:
                        severity = 'INFO'
                    
                    detection = {
                        'time': current_time,
                        'time_fmt': datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S'),
                        'type': event_type,
                        'confidence': conf,
                        'severity': severity,
                        'camera': 'CAM_01',
                        'frame_id': self.frame_count,
                        'bbox': box.xyxy[0].tolist() if box.xyxy is not None else []
                    }
                    detections.append(detection)
        
        # Add to events log
        self.events_log.extend(detections)
        
        # Save to file periodically
        if len(self.events_log) % 10 == 0:
            self.save_events()
    
    def save_events(self):
        """Save events to JSON file"""
        try:
            os.makedirs('data/logs', exist_ok=True)
            with open('data/logs/events.jsonl', 'a') as f:
                for event in self.events_log[-10:]:  # Save last 10 events
                    f.write(json.dumps(event) + '\n')
            print(f"💾 Saved {len(self.events_log[-10:])} events to log")
        except Exception as e:
            print(f"Error saving events: {e}")
    
    def stop_detection(self):
        """Stop detection and cleanup"""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        # Save remaining events
        if self.events_log:
            self.save_events()
        
        print(f"🛑 Detection stopped. Total frames: {self.frame_count}")
        print(f"📊 Total events logged: {len(self.events_log)}")

def main():
    detector = RealTimeYOLODetector()
    
    print("🚀 CAMVIEW.AI Real-Time YOLO Detection")
    print("=" * 50)
    print("1. Start Webcam Detection")
    print("2. Process Video File")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == '1':
        detector.start_webcam_detection()
    elif choice == '2':
        video_path = input("Enter video file path: ")
        if os.path.exists(video_path):
            detector.start_video_detection(video_path)
        else:
            print(f"Error: Video file not found: {video_path}")
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
