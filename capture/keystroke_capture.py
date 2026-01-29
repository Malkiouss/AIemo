from pynput import keyboard
from datetime import datetime
import queue
import threading

class RealTimeKeystrokeCapture:
    """
    Capture keystrokes in real-time for live emotion detection.
    """
    
    def __init__(self, window_size=50):
        self.window_size = window_size  # Number of keystrokes to analyze
        self.keystroke_buffer = []
        self.press_times = {}
        self.callbacks = []
        self.is_running = False
        
    def add_callback(self, callback):
        """Add a callback function to be called when window is full"""
        self.callbacks.append(callback)
    
    def on_press(self, key):
        """Handle key press event"""
        try:
            key_name = key.char if hasattr(key, 'char') else str(key)
            self.press_times[key_name] = datetime.now().timestamp()
        except:
            pass
    
    def on_release(self, key):
        """Handle key release event"""
        try:
            key_name = key.char if hasattr(key, 'char') else str(key)
            
            if key_name in self.press_times:
                release_time = datetime.now().timestamp()
                press_time = self.press_times[key_name]
                
                keystroke = {
                    'key': key_name,
                    'press_time': press_time,
                    'release_time': release_time
                }
                
                self.keystroke_buffer.append(keystroke)
                del self.press_times[key_name]
                
                # Keep buffer at window size
                if len(self.keystroke_buffer) > self.window_size:
                    self.keystroke_buffer.pop(0)
                
                # Trigger callbacks when buffer is full
                if len(self.keystroke_buffer) == self.window_size:
                    for callback in self.callbacks:
                        callback(self.keystroke_buffer.copy())
        except:
            pass
    
    def start(self):
        """Start capturing keystrokes"""
        self.is_running = True
        print("🎹 Keystroke capture started...")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
    
    def stop(self):
        """Stop capturing"""
        self.is_running = False
        print("⏹️  Keystroke capture stopped.")