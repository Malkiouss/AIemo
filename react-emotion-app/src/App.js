import React, { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';
import './App.css';


// At the top of the file
const API_URL = process.env.REACT_APP_API_URL || '/api';



const EMOTION_COLORS = {
  neutral: '#E8E8E8',
  stressed: '#FF6B6B',
  excited: '#4ECDC4',
  tired: '#FFE66D',
};

const EMOTION_LABELS = {
  neutral: 'Neutral',
  stressed: 'Stressed',
  excited: 'Excited',
  tired: 'Tired',
};

function App() {
  const [keystrokes, setKeystrokes] = useState([]);
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const [emotionData, setEmotionData] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [keystrokeCount, setKeystrokeCount] = useState(0);
  const [activeTab, setActiveTab] = useState('emotions');
  const [textContent, setTextContent] = useState('');

  const pressTimes = React.useRef({});
  const textareaRef = React.useRef(null);

  // Handle keydown
  const handleKeyDown = useCallback((e) => {
    pressTimes.current[e.key] = performance.now() / 1000;
  }, []);

  // Handle keyup
  const handleKeyUp = useCallback((e) => {
    if (pressTimes.current[e.key]) {
      const releaseTime = performance.now() / 1000;
      const pressTime = pressTimes.current[e.key];

      const newKeystroke = {
        key: e.key,
        press_time: pressTime,
        release_time: releaseTime,
      };

      setKeystrokes((prev) => {
        const updated = [...prev, newKeystroke];
        if (updated.length > 50) {
          return updated.slice(-50);
        }
        return updated;
      });

      setKeystrokeCount((prev) => prev + 1);
      delete pressTimes.current[e.key];
    }
  }, []);

  // Focus textarea on mount
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  }, []);

  // Reset/Redo test function
  const handleRedoTest = () => {
    setKeystrokes([]);
    setCurrentEmotion(null);
    setEmotionData([]);
    setKeystrokeCount(0);
    setTextContent('');
    setIsAnalyzing(false);
    setActiveTab('emotions');

    // Refocus textarea after reset
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  // Analyze emotion when we have enough keystrokes
  const analyzeEmotion = useCallback(async () => {
    setIsAnalyzing(true);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keystrokes: keystrokes.slice(-50) }),
      });

      const data = await response.json();

      // Transform probabilities into chart data
      const chartData = Object.entries(data.probabilities).map(([emotion, probability]) => ({
        name: EMOTION_LABELS[emotion],
        value: probability * 100,
        emotion: emotion,
        percentage: (probability * 100).toFixed(2),
      }));

      setEmotionData(chartData);
      setCurrentEmotion({
        emotion: data.emotion,
        confidence: (data.confidence * 100).toFixed(2),
      });
    } catch (error) {
      console.error('Error analyzing emotion:', error);
    } finally {
      setIsAnalyzing(false);
    }
  }, [keystrokes]);

  // Analyze emotion when we have enough keystrokes
  useEffect(() => {
    if (keystrokes.length >= 50) {
      analyzeEmotion();
    }
  }, [keystrokes, analyzeEmotion]);

  const renderCustomLabel = ({ cx, cy }) => {
    if (!currentEmotion) return null;

    return (
      <g>
        <text x={cx} y={cy - 10} textAnchor="middle" dominantBaseline="middle" className="chart-center-label">
          Dominant Emotion
        </text>
        <text x={cx} y={cy + 15} textAnchor="middle" dominantBaseline="middle" className="chart-center-emotion">
          {EMOTION_LABELS[currentEmotion.emotion]}
        </text>
        <text x={cx} y={cy + 40} textAnchor="middle" dominantBaseline="middle" className="chart-center-percentage">
          {currentEmotion.confidence}%
        </text>
      </g>
    );
  };

  const CustomLegend = ({ payload }) => {
    return (
      <div className="custom-legend">
        {payload.map((entry, index) => (
          <div key={`legend-${index}`} className="legend-item">
            <span
              className="legend-color"
              style={{ backgroundColor: entry.color }}
            ></span>
            <span className="legend-label">{entry.value}:</span>
            <span className="legend-percentage">{entry.payload.percentage}%</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">Keystroke Emotion Analyzer</h1>
          <p className="app-subtitle">Real-time emotion detection through typing patterns</p>
        </div>
        <div className="keystroke-counter">
          <span className="counter-label">{keystrokes.length >= 50 ? 'Ready' : 'Keys Needed'}</span>
          <span className="counter-value">
            {keystrokes.length >= 50 ? '✓' : Math.max(0, 50 - keystrokes.length)}
          </span>
        </div>
      </header>

      <main className="app-main">
        <section className="content-section">
          <div className="instruction-card">
            <h2>How it works</h2>
            <p>
              Start typing in the text box below. Our AI analyzes your typing rhythm,
              speed, and patterns to detect your emotional state in real-time.
            </p>

            <div className="typing-area">
              <div className="textarea-counter">
                <span className="counter-text">
                  {keystrokes.length >= 50
                    ? `✓ Analysis active (${keystrokeCount} total keystrokes)`
                    : `${Math.max(0, 50 - keystrokes.length)} more keystrokes needed`
                  }
                </span>
              </div>
              <textarea
                ref={textareaRef}
                className="typing-textarea"
                placeholder="Start typing here... Express your thoughts, write anything you want!"
                value={textContent}
                onChange={(e) => setTextContent(e.target.value)}
                onKeyDown={handleKeyDown}
                onKeyUp={handleKeyUp}
                rows={8}
              />
            </div>

            <div className="status-indicator">
              <div className={`status-dot ${keystrokes.length >= 50 ? 'active' : ''}`}></div>
              <span className="status-text">
                {keystrokes.length < 50
                  ? `Type ${50 - keystrokes.length} more keys to begin analysis`
                  : isAnalyzing
                    ? 'Analyzing...'
                    : 'Active monitoring'}
              </span>
            </div>

            {keystrokeCount > 0 && (
              <div className="action-buttons">
                <button className="redo-button" onClick={handleRedoTest}>
                  <span className="button-icon">🔄</span>
                  <span className="button-text">Redo Test</span>
                </button>
              </div>
            )}
          </div>

          {currentEmotion && (
            <div className="insights-card">
              <h3>Current State</h3>
              <div className="emotion-badge" style={{
                backgroundColor: EMOTION_COLORS[currentEmotion.emotion] + '20',
                borderColor: EMOTION_COLORS[currentEmotion.emotion]
              }}>
                <span className="emotion-name">{EMOTION_LABELS[currentEmotion.emotion]}</span>
                <span className="emotion-confidence">{currentEmotion.confidence}% confidence</span>
              </div>
            </div>
          )}
        </section>

        <section className="visualization-section">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'emotions' ? 'active' : ''}`}
              onClick={() => setActiveTab('emotions')}
            >
              Emotions
            </button>
            <button
              className={`tab ${activeTab === 'insights' ? 'active' : ''}`}
              onClick={() => setActiveTab('insights')}
            >
              Insights
            </button>
          </div>

          {activeTab === 'emotions' && emotionData.length > 0 && (
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={460}>
                <PieChart margin={{ top: 50 }}>
                  <Pie
                    data={emotionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={90}
                    outerRadius={150}
                    paddingAngle={3}
                    dataKey="value"
                    label={renderCustomLabel}
                  >
                    {emotionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={EMOTION_COLORS[entry.emotion]} />
                    ))}
                  </Pie>
                  <Legend content={<CustomLegend />} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}

          {activeTab === 'insights' && (
            <div className="insights-panel">
              <h3>Typing Patterns</h3>
              <p>Analysis based on {keystrokeCount} total keystrokes</p>
              <div className="pattern-grid">
                <div className="pattern-card">
                  <span className="pattern-icon">⚡</span>
                  <span className="pattern-label">Typing Speed</span>
                  <span className="pattern-value">
                    {keystrokes.length >= 2
                      ? Math.round(
                        (keystrokes.length /
                          (keystrokes[keystrokes.length - 1].release_time -
                            keystrokes[0].press_time)) *
                        60
                      )
                      : 0}{' '}
                    WPM
                  </span>
                </div>
                <div className="pattern-card">
                  <span className="pattern-icon">📊</span>
                  <span className="pattern-label">Patterns Detected</span>
                  <span className="pattern-value">{keystrokes.length >= 50 ? 'Active' : 'Pending'}</span>
                </div>
              </div>
            </div>
          )}

          {emotionData.length === 0 && (
            <div className="empty-state">
              <div className="empty-icon">⌨️</div>
              <p>Start typing to see your emotional analysis</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;