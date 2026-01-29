import os
import sys

def setup_project():
    """Create project directory structure"""
    dirs = [
        'models/trained_models',
        'data',
        'capture',
        'web/templates'
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Project structure created")

def main():
    print("=" * 70)
    print("KEYSTROKE EMOTION DETECTOR - PROJECT SETUP")
    print("=" * 70)
    
    print("\nWhat would you like to do?\n")
    print("1. Generate synthetic training data")
    print("2. Collect real data (interactive)")
    print("3. Train the model")
    print("4. Start real-time capture (console)")
    print("5. Start web dashboard")
    print("6. Run model comparison")
    
    choice = input("\nEnter choice (1-6): ")
    
    if choice == '1':
        from data.synthetic_data import generate_synthetic_dataset
        generate_synthetic_dataset(n_samples=1000)
        
    elif choice == '2':
        from data.collection_tool import KeystrokeCollector
        collector = KeystrokeCollector()
        collector.collect_data_interactive()
        
    elif choice == '3':
        from models.emotion_detector import EmotionDetector
        detector = EmotionDetector()
        data_file = input("Enter data file path (default: data/synthetic_keystroke_data.json): ")
        data_file = data_file or 'data/synthetic_keystroke_data.json'
        detector.train(data_file)
        detector.save()
        
    elif choice == '4':
        from capture.keystroke_capture import RealTimeKeystrokeCapture
        from models.emotion_detector import EmotionDetector
        
        detector = EmotionDetector()
        detector.load()
        
        def on_window_full(keystrokes):
            emotion, confidence, _ = detector.predict(keystrokes)
            print(f"Detected: {emotion} ({confidence*100:.1f}% confidence)")
        
        capture = RealTimeKeystrokeCapture(window_size=50)
        capture.add_callback(on_window_full)
        capture.start()
        
    elif choice == '5':
        print("\n🌐 Starting web dashboard...")
        print("Open http://localhost:5000 in your browser")
        os.system('python web/app.py')
        
    elif choice == '6':
        print("\n📊 Running model comparison...")
        os.system('python models/model_comparison.py')

if __name__ == "__main__":
    setup_project()
    main()

# ================ ADD THIS AFTER YOUR generate_synthetic_data() FUNCTION ================

class RealTimeEmotionDetector:
    """Simple real-time emotion detector using your best model"""
    
    def __init__(self, model_name='Random Forest'):
        self.scaler = StandardScaler()
        self.model = None
        self.model_name = model_name
        self.predictions_history = []
        
    def set_model(self, model):
        """Set trained model and scaler"""
        self.model = model
        
    def extract_features(self, keystroke_timestamps):
        """
        Extract features from keystroke timestamps
        keystroke_timestamps: list of timestamps in milliseconds
        """
        if len(keystroke_timestamps) < 10:
            return None
            
        # Calculate intervals between keystrokes
        intervals = np.diff(keystroke_timestamps)
        
        features = [
            np.mean(intervals),           # Mean interval
            np.var(intervals),            # Variance
            len([i for i in intervals if i > 500]) / max(len(intervals), 1),  # Pause frequency
            np.mean([i for i in intervals if i > 500]) if any(i > 500 for i in intervals) else 0,  # Mean pause
            np.std(intervals),           # Standard deviation
            np.max(intervals),           # Maximum interval
            np.min(intervals),           # Minimum interval
            np.percentile(intervals, 25), # Q1
            np.percentile(intervals, 75), # Q3
            len(keystroke_timestamps) / ((keystroke_timestamps[-1] - keystroke_timestamps[0]) / 1000) if len(keystroke_timestamps) > 1 else 0,  # Typing speed
            np.std(intervals) / np.mean(intervals) if np.mean(intervals) > 0 else 0,  # CV
            sum(1 for i in intervals if i < 100) / max(len(intervals), 1)  # Burst ratio
        ]
        
        return np.array(features)
    
    def predict(self, keystroke_timestamps):
        """Predict emotion from keystroke timestamps"""
        features = self.extract_features(keystroke_timestamps)
        if features is None:
            return "unknown", 0
            
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        
        # Map prediction to emotion
        emotions = ['neutral', 'stressed', 'excited', 'tired']
        emotion = emotions[prediction] if prediction < len(emotions) else 'unknown'
        
        self.predictions_history.append(emotion)
        if len(self.predictions_history) > 50:
            self.predictions_history = self.predictions_history[-50:]
            
        return emotion, features


def demo_real_time():
    """Simple demo using your trained model"""
    print("\n" + "=" * 70)
    print("REAL-TIME DEMO")
    print("=" * 70)
    
    # 1. Generate and train on data
    X, y = generate_synthetic_data(n_samples=1000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Train Random Forest (your best model)
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    rf_model.fit(X_train_scaled, y_train)
    
    # 3. Create real-time detector
    detector = RealTimeEmotionDetector(model_name='Random Forest')
    detector.model = rf_model
    detector.scaler = scaler
    
    # 4. Generate mock keystrokes for different emotions
    emotions_patterns = {
        'neutral': {'mean_interval': 200, 'std': 40},
        'stressed': {'mean_interval': 150, 'std': 60},
        'excited': {'mean_interval': 120, 'std': 30},
        'tired': {'mean_interval': 300, 'std': 80}
    }
    
    for emotion_name, pattern in emotions_patterns.items():
        print(f"\nSimulating '{emotion_name}' typing pattern:")
        
        # Generate mock keystroke timestamps
        timestamps = [0]
        for i in range(50):  # 50 keystrokes
            interval = np.random.normal(pattern['mean_interval'], pattern['std'])
            interval = max(50, interval)  # Minimum 50ms
            timestamps.append(timestamps[-1] + interval)
        
        # Predict
        predicted_emotion, features = detector.predict(timestamps)
        print(f"  Predicted: {predicted_emotion}")
        print(f"  Features extracted: {len(features)}")
        
    print(f"\nPrediction history (last 5): {detector.predictions_history[-5:]}")


# ================ MODIFY YOUR main() FUNCTION ================

# In your main() function, AFTER comparator.print_summary(), add:

def main():
    # ... (keep all your existing code until after comparator.print_summary())
    
    comparator.print_summary()
    
    # ============ ADD THESE LINES ============
    print("\n" + "=" * 70)
    print("TESTING REAL-TIME CAPABILITIES")
    print("=" * 70)
    
    demo_real_time()
    
    print("\n" + "=" * 70)
    print("PROJECT IMPLEMENTATION STEPS")
    print("=" * 70)
    print("""
    Your next steps:
    1. Collect real keystroke data with timestamps
    2. Label the data with emotions
    3. Replace synthetic_data() with real data loading
    4. Use the RealTimeEmotionDetector class for predictions
    5. Build a simple UI to show emotion in real-time
    """)
    # ============ END OF ADDITION ============