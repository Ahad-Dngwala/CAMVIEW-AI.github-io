"""
Unified Video Processing Service
Handles video processing for both terminal and Streamlit interfaces
"""
import cv2
import time
import threading
from typing import List, Optional, Callable, Dict, Any
from dataclasses import dataclass
from core.events import Event
from core.event_bus import bus
from detectors.yolo_wrapper import BaseDetector
from config import settings
import queue
import json

@dataclass
class ProcessingStatus:
    """Real-time processing status"""
    is_processing: bool = False
    current_frame: int = 0
    total_frames: int = 0
    fps: float = 30.0
    events_detected: int = 0
    processing_time: float = 0.0
    last_update: float = 0.0

class UnifiedVideoProcessor:
    """Unified video processor for both terminal and Streamlit"""
    
    def __init__(self, detectors: List[BaseDetector] = None):
        self.detectors = detectors or []
        self.status = ProcessingStatus()
        self.video_source = None
        self.cap = None
        self.processing_thread = None
        self.frame_callback = None
        self.event_callback = None
        self.stop_event = threading.Event()
        self.frame_queue = queue.Queue(maxsize=30)  # Buffer for frames
        self.stats_lock = threading.Lock()
        
    def set_detectors(self, detectors: List[BaseDetector]):
        """Update detectors dynamically"""
        self.detectors = detectors
        
    def set_callbacks(self, frame_callback: Callable = None, event_callback: Callable = None):
        """Set callbacks for frame and event updates"""
        self.frame_callback = frame_callback
        self.event_callback = event_callback
        
    def set_frame_buffer(self, max_size: int = 30):
        """Set frame buffer size for preview"""
        self.frame_queue = queue.Queue(maxsize=max_size)
        
    def load_video(self, source):
        """Load video source (file path or camera index)"""
        try:
            if isinstance(source, str):
                self.video_source = source
                self.cap = cv2.VideoCapture(source)
                if self.cap.isOpened():
                    self.status.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.status.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
                    return True
            elif isinstance(source, int):
                self.video_source = source
                self.cap = cv2.VideoCapture(source)
                return self.cap.isOpened()
        except Exception as e:
            print(f"[ERROR] Failed to load video source {source}: {e}")
        return False
    
    def start_processing(self):
        """Start video processing in background thread"""
        if self.cap is None or not self.cap.isOpened():
            return False
            
        self.stop_event.clear()
        self.status.is_processing = True
        self.status.current_frame = 0
        self.status.events_detected = 0
        self.status.processing_time = time.time()
        
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        return True
    
    def stop_processing(self):
        """Stop video processing"""
        self.stop_event.set()
        self.status.is_processing = False
        
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2.0)
            
        if self.cap:
            self.cap.release()
            
    def _processing_loop(self):
        """Main processing loop running in background thread"""
        start_time = time.time()
        
        while not self.stop_event.is_set() and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
                
            self.status.current_frame += 1
            frame_start = time.time()
            
            # Process frame through all detectors
            events = []
            processed_frame = frame.copy()
            
            for detector in self.detectors:
                try:
                    detector_events = detector.process(processed_frame, self.status.current_frame)
                    events.extend(detector_events)
                    
                    # Publish events to bus
                    for event in detector_events:
                        bus.publish(event)
                        
                except Exception as e:
                    print(f"[ERROR] Detector failed: {e}")
            
            # Add frame info overlay
            cv2.putText(processed_frame, f"Frame: {self.status.current_frame}", 
                       (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add event count overlay
            if events:
                cv2.putText(processed_frame, f"Events: {len(events)}", 
                           (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # Update statistics
            with self.stats_lock:
                self.status.events_detected += len(events)
                self.status.last_update = time.time()
            
            # Send frame via callback (for Streamlit)
            if self.frame_callback:
                try:
                    self.frame_callback(processed_frame, events)
                except Exception as e:
                    print(f"[ERROR] Frame callback failed: {e}")
            
            # Store frame in queue for Streamlit preview
            try:
                # Clear old frames if queue is full
                while self.frame_queue.qsize() >= self.frame_queue.maxsize:
                    self.frame_queue.get_nowait()
                self.frame_queue.put(processed_frame, timeout=0.01)
            except queue.Full:
                pass  # Skip frame if queue is full
            except Exception as e:
                print(f"[ERROR] Frame queue error: {e}")
            
            # Send events via callback
            if self.event_callback and events:
                try:
                    self.event_callback(events)
                except Exception as e:
                    print(f"[ERROR] Event callback failed: {e}")
            
            # Control frame rate for real-time processing
            processing_time = time.time() - frame_start
            target_delay = 1.0 / self.status.fps
            if processing_time < target_delay:
                time.sleep(target_delay - processing_time)
        
        # Processing completed
        self.status.is_processing = False
        self.status.processing_time = time.time() - start_time
        
    def get_status(self) -> ProcessingStatus:
        """Get current processing status"""
        with self.stats_lock:
            return ProcessingStatus(
                is_processing=self.status.is_processing,
                current_frame=self.status.current_frame,
                total_frames=self.status.total_frames,
                fps=self.status.fps,
                events_detected=self.status.events_detected,
                processing_time=self.status.processing_time,
                last_update=self.status.last_update
            )
    
    def get_frame(self) -> Optional[Any]:
        """Get latest processed frame (non-blocking)"""
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None

# Global processor instance
_processor_instance = None

def get_processor() -> UnifiedVideoProcessor:
    """Get or create global processor instance"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = UnifiedVideoProcessor()
    return _processor_instance
