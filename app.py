from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.emotion_detector import EmotionDetector

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

detector = EmotionDetector()

# Load pre-trained model
try:
    detector.load('models/trained_models/emotion_detector.pkl')
    print(f"✅ Model loaded. Emotion labels: {detector.emotion_labels}")
except Exception as e:
    print(f"⚠️ No trained model found. Please train first. Error: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for emotion prediction"""
    try:
        keystroke_data = request.json['keystrokes']
        
        emotion, confidence, probabilities = detector.predict(keystroke_data)
        
        # Ensure emotion is lowercase for consistency
        emotion = emotion.lower() if isinstance(emotion, str) else emotion
        
        # Build probabilities dictionary with lowercase keys
        prob_dict = {}
        for i, label in enumerate(detector.emotion_labels):
            label_lower = label.lower() if isinstance(label, str) else str(label)
            prob_dict[label_lower] = float(probabilities[i])
        
        print(f"Prediction: {emotion}, Confidence: {confidence:.2f}")
        print(f"Probabilities: {prob_dict}")
        
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

@app.route('/stats')
def stats():
    """Get model statistics"""
    return jsonify({
        'trained': detector.is_trained,
        'emotions': [label.lower() for label in detector.emotion_labels],
        'model_type': 'Random Forest'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'model_loaded': detector.is_trained})

if __name__ == '__main__':
    app.run(debug=True, port=5000)