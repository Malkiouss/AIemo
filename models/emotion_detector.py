import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import json

class EmotionDetector:
    """
    Enhanced emotion detector with training, prediction, and persistence.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.emotion_labels = ['neutral', 'stressed', 'excited', 'tired']
        self.is_trained = False
        
    def extract_features(self, keystroke_data):
        """Extract 12 timing features from keystroke sequence"""
        if len(keystroke_data) < 2:
            return None
        
        # Calculate timing metrics
        dwell_times = [k['release_time'] - k['press_time'] for k in keystroke_data]
        flight_times = [
            keystroke_data[i+1]['press_time'] - keystroke_data[i]['release_time']
            for i in range(len(keystroke_data)-1)
        ]
        
        features = {
            'avg_dwell': np.mean(dwell_times),
            'std_dwell': np.std(dwell_times),
            'max_dwell': np.max(dwell_times),
            'min_dwell': np.min(dwell_times),
            'avg_flight': np.mean(flight_times),
            'std_flight': np.std(flight_times),
            'max_flight': np.max(flight_times),
            'min_flight': np.min(flight_times),
            'typing_speed': len(keystroke_data) / (keystroke_data[-1]['release_time'] - keystroke_data[0]['press_time']),
            'backspace_rate': sum(1 for k in keystroke_data if k['key'] == 'Backspace') / len(keystroke_data),
            'flight_cv': np.std(flight_times) / (np.mean(flight_times) + 1e-6),
            'dwell_cv': np.std(dwell_times) / (np.mean(dwell_times) + 1e-6),
        }
        
        return list(features.values())
    
    def train(self, data_path):
        """Train model from JSON data file"""
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        X = []
        y = []
        
        for sample in data:
            features = self.extract_features(sample['keystrokes'])
            if features:
                X.append(features)
                y.append(sample['emotion'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale and train
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        print(f"✅ Model trained on {len(X)} samples")
        return self
    
    def predict(self, keystroke_data):
        """
        Predict emotion from keystroke sequence
        
        FIXED: Now correctly selects emotion with highest probability
        """
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        features = self.extract_features(keystroke_data)
        if features is None:
            return None, 0, []
        
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        # Get probabilities for all emotions
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # ✅ FIX: Select emotion with HIGHEST probability
        predicted_idx = int(probabilities.argmax())
        emotion = self.emotion_labels[predicted_idx]
        confidence = float(probabilities[predicted_idx])
        
        return emotion, confidence, probabilities
    
    def save(self, model_path='models/trained_models/emotion_detector.pkl'):
        """Save trained model"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'emotions': self.emotion_labels
        }, model_path)
        print(f"💾 Model saved to {model_path}")
    
    def load(self, model_path='models/trained_models/emotion_detector.pkl'):
        """Load trained model"""
        data = joblib.load(model_path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.emotion_labels = data['emotions']
        self.is_trained = True
        print(f"📂 Model loaded from {model_path}")
        return self