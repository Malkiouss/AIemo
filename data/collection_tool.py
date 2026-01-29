import json
from datetime import datetime
from pynput import keyboard

class KeystrokeCollector:
    """
    Tool for collecting real keystroke data with emotion labels.
    Use this to gather data from volunteers.
    """
    
    def __init__(self, output_file='data/collected_data.json'):
        self.output_file = output_file
        self.current_session = []
        self.press_times = {}
        self.is_recording = False
        self.current_emotion = None
        
    def on_press(self, key):
        """Record key press time"""
        if not self.is_recording:
            return
            
        try:
            key_name = key.char if hasattr(key, 'char') else str(key)
            self.press_times[key_name] = datetime.now().timestamp()
        except:
            pass
    
    def on_release(self, key):
        """Record key release and calculate dwell time"""
        if not self.is_recording:
            return
            
        try:
            key_name = key.char if hasattr(key, 'char') else str(key)
            
            if key_name in self.press_times:
                release_time = datetime.now().timestamp()
                press_time = self.press_times[key_name]
                
                self.current_session.append({
                    'key': key_name,
                    'press_time': press_time,
                    'release_time': release_time
                })
                
                del self.press_times[key_name]
        except:
            pass
    
    def start_recording(self, emotion):
        """Start recording keystroke data"""
        self.current_emotion = emotion
        self.current_session = []
        self.press_times = {}
        self.is_recording = True
        print(f"\n🔴 Recording started for emotion: {emotion}")
        print("Type naturally for 30-60 seconds...")
        print("Press ESC when done.\n")
    
    def stop_recording(self):
        """Stop recording and save data"""
        self.is_recording = False
        
        if len(self.current_session) > 10:
            # Load existing data
            try:
                with open(self.output_file, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            # Add new session
            session_id = f"{self.current_emotion}_{len(data)}"
            data.append({
                'id': session_id,
                'emotion': self.current_emotion,
                'keystrokes': self.current_session,
                'timestamp': datetime.now().isoformat()
            })
            
            # Save
            with open(self.output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"\n✅ Session saved! Captured {len(self.current_session)} keystrokes")
            return True
        else:
            print("\n❌ Session too short. Please type more.")
            return False
    
    def collect_data_interactive(self):
        """Interactive data collection session"""
        print("=" * 60)
        print("KEYSTROKE DATA COLLECTION TOOL")
        print("=" * 60)
        print("\nThis tool will help you collect labeled keystroke data.")
        print("You'll be asked to type while experiencing different emotions.")
        
        emotions = ['neutral', 'stressed', 'excited', 'tired']
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            for emotion in emotions:
                input(f"\nPress ENTER when you're ready to record '{emotion}' typing...")
                self.start_recording(emotion)
                
                # Wait for ESC
                keyboard_listener = keyboard.Listener(
                    on_press=lambda key: listener.stop() if key == keyboard.Key.esc else None
                )
                keyboard_listener.start()
                keyboard_listener.join()
                
                self.stop_recording()
        
        print("\n" + "=" * 60)
        print("Data collection complete!")
        print(f"Data saved to: {self.output_file}")