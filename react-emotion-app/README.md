# Keystroke Emotion Analyzer - React Frontend

Beautiful, modern React frontend with donut chart visualization for real-time emotion detection through typing patterns.

## 🎨 Features

- **Real-time Analysis**: Captures keystrokes and analyzes emotional state in real-time
- **Beautiful Donut Chart**: Inspired by modern analytics dashboards
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Theme**: Professional dark mode with smooth animations
- **Live Statistics**: Real-time keystroke counting and WPM calculation
- **Multiple Views**: Emotions and Insights tabs for different perspectives

## 📋 Prerequisites

1. **Node.js** (v14 or higher)
2. **Python 3.7+** with Flask backend
3. **Trained emotion detection model**

## 🚀 Quick Start

### Step 1: Set Up the Backend

First, make sure your Flask backend has CORS enabled:

```bash
# Install Flask-CORS
pip install flask-cors
```

Replace your `web/app.py` with the provided `app_with_cors.py`:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS
```

Start the Flask backend:

```bash
python web/app.py
# Should run on http://localhost:5000
```

### Step 2: Set Up the React Frontend

Navigate to the React app directory and install dependencies:

```bash
cd react-emotion-app
npm install
```

Start the development server:

```bash
npm start
```

The app will open at `http://localhost:3000`

## 📁 Project Structure

```
react-emotion-app/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── App.js              # Main component with chart
│   ├── App.css             # Styling
│   ├── index.js            # React entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies
└── README.md               # This file
```

## 🎯 How It Works

1. **Start Typing**: Simply start typing on your keyboard
2. **Data Collection**: The app captures keystroke timing data (press and release times)
3. **Analysis**: After 50 keystrokes, the data is sent to the Flask backend
4. **Visualization**: Results are displayed in a beautiful donut chart
5. **Real-time Updates**: Continue typing to see updates in real-time

## 🎨 Design Philosophy

This design avoids generic AI aesthetics by using:

- **Typography**: Manrope (display) + JetBrains Mono (monospace)
- **Color Scheme**: Dark theme with cyan accent (not purple gradients!)
- **Animations**: Smooth, purposeful animations using CSS
- **Layout**: Two-column responsive grid inspired by modern dashboards
- **Visual Hierarchy**: Clear emphasis on the donut chart and key metrics

## 🔧 Customization

### Changing Colors

Edit `App.css` variables:

```css
:root {
  --color-accent: #4ECDC4;      /* Primary accent color */
  --emotion-neutral: #E8E8E8;   /* Neutral emotion color */
  --emotion-stressed: #FF6B6B;  /* Stressed emotion color */
  --emotion-excited: #4ECDC4;   /* Excited emotion color */
  --emotion-tired: #FFE66D;     /* Tired emotion color */
}
```

### Adding New Emotions

1. Update the Flask backend to return new emotions
2. Add color mapping in `App.js`:

```javascript
const EMOTION_COLORS = {
  neutral: '#E8E8E8',
  stressed: '#FF6B6B',
  excited: '#4ECDC4',
  tired: '#FFE66D',
  happy: '#95E1D3',  // New emotion
};
```

3. Add label mapping:

```javascript
const EMOTION_LABELS = {
  neutral: 'Neutral',
  stressed: 'Stressed',
  excited: 'Excited',
  tired: 'Tired',
  happy: 'Happy',  // New label
};
```

### Adjusting Chart Size

In `App.js`, modify the ResponsiveContainer height:

```javascript
<ResponsiveContainer width="100%" height={500}>
  {/* Increase from 400 to 500 */}
</ResponsiveContainer>
```

## 🐛 Troubleshooting

### Issue: CORS Error

**Problem**: Console shows "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution**: 
1. Install Flask-CORS: `pip install flask-cors`
2. Add to your Flask app:
```python
from flask_cors import CORS
CORS(app)
```

### Issue: Connection Refused

**Problem**: Cannot connect to Flask backend

**Solution**: 
1. Ensure Flask is running on port 5000
2. Check `package.json` has `"proxy": "http://localhost:5000"`
3. Restart both servers

### Issue: Chart Not Showing

**Problem**: Empty state shows even after typing

**Solution**: 
1. Check browser console for errors
2. Verify Flask endpoint returns correct data format
3. Ensure you've typed at least 50 characters

### Issue: Slow Performance

**Problem**: App feels sluggish

**Solution**: 
1. Check if keystroke buffer is growing too large
2. Verify model inference time in Flask
3. Consider reducing chart animation duration

## 📊 API Integration

The React app expects this API response format:

```json
{
  "emotion": "stressed",
  "confidence": 0.48,
  "probabilities": {
    "neutral": 0.01,
    "stressed": 0.48,
    "excited": 0.31,
    "tired": 0.20
  }
}
```

### Required Endpoints

1. **POST /predict**
   - Receives: `{ "keystrokes": [...] }`
   - Returns: Emotion prediction with probabilities

2. **GET /stats** (optional)
   - Returns: Model information
   - Used for initial model status check

3. **GET /health** (optional)
   - Returns: `{ "status": "ok", "model_loaded": true }`

## 🎓 Learning Resources

- **Recharts Documentation**: https://recharts.org/
- **React Hooks**: https://react.dev/reference/react
- **CSS Animations**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations

## 📝 Development Notes

### State Management

The app uses React hooks for state management:
- `keystrokes`: Array of keystroke objects
- `currentEmotion`: Latest emotion prediction
- `emotionData`: Chart data array
- `keystrokeCount`: Total keystrokes captured

### Performance Considerations

- Keystroke buffer limited to last 50 keystrokes
- Debounced API calls (only on keystroke 50+)
- CSS animations use `transform` and `opacity` for GPU acceleration
- Chart re-renders only when data changes

### Browser Compatibility

Tested on:
- ✅ Chrome 120+
- ✅ Firefox 120+
- ✅ Safari 17+
- ✅ Edge 120+

## 🚢 Production Build

To create a production build:

```bash
npm run build
```

This creates an optimized build in the `build/` folder.

To serve it:

```bash
# Option 1: Using serve
npx serve -s build

# Option 2: Integrate with Flask
# Copy build folder to Flask static directory
```

### Integrating with Flask

To serve React from Flask:

```python
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory('build', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('build', path)
```

## 📜 License

This project is part of the Keystroke Emotion Detector system.

## 🤝 Contributing

Feel free to submit issues or pull requests!

## 📧 Support

For issues or questions, check the troubleshooting section above or create an issue in the repository.

---

**Built with ❤️ using React, Recharts, and modern web technologies**
