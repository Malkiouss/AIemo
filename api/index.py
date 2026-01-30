from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.emotion_detector import EmotionDetector

app = Flask(__name__)

# Enable CORS for all origins (update with specific frontend URL after deployment)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize detector globally
detector = EmotionDetector()
model_loaded = False

def load_model():
    """Load model on cold start"""
    global model_loaded
    if not model_loaded:
        try:
            # Try multiple possible paths for Vercel
            possible_paths = [
                'models/trained_models/emotion_detector.pkl',
                '../models/trained_models/emotion_detector.pkl',
                os.path.join(os.path.dirname(__file__), '..', 'models', 'trained_models', 'emotion_detector.pkl'),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    detector.load(path)
                    model_loaded = True
                    print(f"✅ Model loaded from: {path}")
                    return True
            
            print("⚠️ Model file not found")
            return False
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            return False
    return model_loaded

# Load model on import
load_model()

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict emotion from keystrokes"""
    if not model_loaded or not detector.is_trained:
        return jsonify({
            'error': 'Model not loaded',
            'emotion': 'neutral',
            'confidence': 0.0,
            'probabilities': {'neutral': 0.25, 'stressed': 0.25, 'excited': 0.25, 'tired': 0.25}
        }), 503
    
    try:
        keystroke_data = request.json.get('keystrokes', [])
        
        if len(keystroke_data) < 2:
            return jsonify({
                'error': 'Not enough keystroke data',
                'emotion': 'neutral',
                'confidence': 0.0,
                'probabilities': {'neutral': 0.25, 'stressed': 0.25, 'excited': 0.25, 'tired': 0.25}
            }), 400
        
        emotion, confidence, probabilities = detector.predict(keystroke_data)
        
        # Ensure lowercase
        emotion = emotion.lower() if isinstance(emotion, str) else str(emotion).lower()
        
        # Build probabilities dictionary
        prob_dict = {}
        for i, label in enumerate(detector.emotion_labels):
            label_lower = label.lower() if isinstance(label, str) else str(label).lower()
            prob_dict[label_lower] = float(probabilities[i])
        
        return jsonify({
            'emotion': emotion,
            'confidence': float(confidence),
            'probabilities': prob_dict
        })
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({
            'error': str(e),
            'emotion': 'neutral',
            'confidence': 0.0,
            'probabilities': {'neutral': 0.25, 'stressed': 0.25, 'excited': 0.25, 'tired': 0.25}
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model_loaded and detector.is_trained,
        'environment': 'vercel-serverless'
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get model statistics"""
    return jsonify({
        'trained': detector.is_trained if model_loaded else False,
        'emotions': [label.lower() for label in detector.emotion_labels] if model_loaded else [],
        'model_type': 'Random Forest' if model_loaded else 'Not loaded'
    })



# For local testing
if __name__ == '__main__':
    app.run(debug=True)