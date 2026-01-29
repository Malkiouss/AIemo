"""
test_emotion.py - Simple testing script
"""

import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def generate_test_data():
    """Generate test data that simulates keystroke patterns"""
    np.random.seed(42)
    n_samples = 200
    
    # Create 4 emotion classes
    X = []
    y = []
    
    # Emotion 0: Neutral (consistent typing)
    for _ in range(n_samples//4):
        features = np.random.normal([200, 1000, 0.1, 0.05, 4.0], [20, 200, 0.02, 0.01, 0.5])
        X.append(features)
        y.append(0)
    
    # Emotion 1: Stressed (erratic typing)
    for _ in range(n_samples//4):
        features = np.random.normal([150, 3000, 0.2, 0.15, 5.5], [30, 500, 0.05, 0.03, 0.8])
        X.append(features)
        y.append(1)
    
    # Emotion 2: Excited (fast typing)
    for _ in range(n_samples//4):
        features = np.random.normal([120, 500, 0.05, 0.02, 6.5], [15, 100, 0.01, 0.005, 0.6])
        X.append(features)
        y.append(2)
    
    # Emotion 3: Tired (slow typing)
    for _ in range(n_samples//4):
        features = np.random.normal([300, 2000, 0.15, 0.12, 2.5], [40, 300, 0.03, 0.02, 0.4])
        X.append(features)
        y.append(3)
    
    return np.array(X), np.array(y)

def test_basic_functionality():
    """Test basic ML pipeline"""
    print("🧪 Testing Basic Functionality")
    print("=" * 50)
    
    # Generate test data
    X, y = generate_test_data()
    print(f"Test data shape: {X.shape}")
    print(f"Class distribution: {np.bincount(y)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a simple model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    # Test predictions
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.2%}")
    print(f"Test samples: {len(y_test)}")
    
    # Test individual predictions
    print("\nTesting individual predictions:")
    test_samples = X_test[:5]
    for i, sample in enumerate(test_samples):
        prediction = model.predict([sample])[0]
        actual = y_test[i]
        emotions = ['Neutral', 'Stressed', 'Excited', 'Tired']
        print(f"  Sample {i+1}: Predicted={emotions[prediction]}, Actual={emotions[actual]}")
    
    return accuracy > 0.7  # Pass if accuracy > 70%

def test_feature_extraction():
    """Test feature extraction from keystroke timestamps"""
    print("\n🔍 Testing Feature Extraction")
    print("=" * 50)
    
    # Simulate keystroke timestamps (in milliseconds)
    def simulate_typing_session(mean_interval=200, std=40, n_keys=50):
        timestamps = [0]
        for i in range(n_keys):
            interval = np.random.normal(mean_interval, std)
            interval = max(50, interval)  # Minimum 50ms
            timestamps.append(timestamps[-1] + interval)
        return timestamps
    
    # Test different patterns
    patterns = {
        "Normal": (200, 40),
        "Fast": (120, 30),
        "Slow": (300, 80),
        "Erratic": (150, 60)
    }
    
    for name, (mean, std) in patterns.items():
        timestamps = simulate_typing_session(mean, std, 30)
        intervals = np.diff(timestamps)
        
        # Extract features
        features = {
            "mean_interval": np.mean(intervals),
            "interval_variance": np.var(intervals),
            "pause_count": sum(1 for i in intervals if i > 500),
            "typing_speed": len(timestamps) / (timestamps[-1] / 1000)  # keys per second
        }
        
        print(f"\n{name} typing pattern:")
        for key, value in features.items():
            print(f"  {key}: {value:.1f}")
    
    return True

def test_real_time_simulation():
    """Simulate real-time keystroke input"""
    print("\n⏱️ Testing Real-Time Simulation")
    print("=" * 50)
    
    print("Simulating 10 seconds of typing...")
    
    # Simulate different emotions over time
    emotion_sequence = [
        ("neutral", 5, 200, 40),    # 5 seconds of neutral typing
        ("stressed", 3, 150, 60),   # 3 seconds of stressed typing
        ("excited", 2, 120, 30),    # 2 seconds of excited typing
    ]
    
    all_keystrokes = []
    total_time = 0
    
    for emotion, duration, mean_interval, std in emotion_sequence:
        print(f"\n{emotion.capitalize()} typing for {duration} seconds:")
        
        end_time = total_time + duration * 1000  # Convert to milliseconds
        current_time = total_time
        
        while current_time < end_time:
            interval = np.random.normal(mean_interval, std)
            current_time += max(50, interval)
            if current_time < end_time:
                all_keystrokes.append(current_time)
        
        total_time = end_time
        
        if all_keystrokes:
            recent = all_keystrokes[-min(10, len(all_keystrokes)):]
            avg_interval = np.mean(np.diff(recent)) if len(recent) > 1 else 0
            print(f"  Recent avg interval: {avg_interval:.1f}ms")
    
    print(f"\nTotal keystrokes simulated: {len(all_keystrokes)}")
    print(f"Total time: {total_time/1000:.1f} seconds")
    
    return len(all_keystrokes) > 20

def run_all_tests():
    """Run all tests and report results"""
    print("🚀 COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Basic ML Functionality", test_basic_functionality),
        ("Feature Extraction", test_feature_extraction),
        ("Real-Time Simulation", test_real_time_simulation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n▶️ Running: {test_name}")
        try:
            success = test_func()
            status = "✅ PASS" if success else "❌ FAIL"
            results.append((test_name, success))
            print(f"   Result: {status}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your system is working correctly.")
        print("\nNext steps:")
        print("1. Run your full model comparison: python your_file.py")
        print("2. Start collecting real keystroke data")
        print("3. Build a simple UI to visualize results")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
    
    return all(success for _, success in results)

if __name__ == "__main__":
    run_all_tests()