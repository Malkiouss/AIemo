import numpy as np
import pandas as pd
import json

def generate_synthetic_dataset(n_samples=1000, save_path='data/synthetic_keystroke_data.json'):
    """
    Generate realistic synthetic keystroke data for emotion detection.
    
    Parameters:
    - n_samples: Total number of samples to generate
    - save_path: Where to save the generated data
    
    Returns:
    - keystroke_data: List of keystroke sequences
    - emotion_labels: Corresponding emotion labels
    """
    np.random.seed(42)
    
    # Define emotional typing patterns based on research
    emotion_patterns = {
        'neutral': {
            'dwell_mean': 0.08, 'dwell_std': 0.02,
            'flight_mean': 0.15, 'flight_std': 0.05,
            'speed': 4.5,
            'error_rate': 0.02,
            'rhythm_variability': 0.3
        },
        'stressed': {
            'dwell_mean': 0.06, 'dwell_std': 0.03,
            'flight_mean': 0.12, 'flight_std': 0.08,
            'speed': 5.5,
            'error_rate': 0.08,
            'rhythm_variability': 0.7
        },
        'excited': {
            'dwell_mean': 0.05, 'dwell_std': 0.025,
            'flight_mean': 0.10, 'flight_std': 0.06,
            'speed': 6.0,
            'error_rate': 0.06,
            'rhythm_variability': 0.6
        },
        'tired': {
            'dwell_mean': 0.12, 'dwell_std': 0.04,
            'flight_mean': 0.25, 'flight_std': 0.10,
            'speed': 3.0,
            'error_rate': 0.03,
            'rhythm_variability': 0.4
        }
    }
    
    all_data = []
    
    for emotion, params in emotion_patterns.items():
        for sample_id in range(n_samples // 4):
            # Generate a typing sequence (30-50 keystrokes)
            seq_length = np.random.randint(30, 50)
            keystrokes = []
            current_time = 0.0
            
            for i in range(seq_length):
                # Choose a key
                if np.random.random() < params['error_rate']:
                    key = 'Backspace'
                else:
                    key = np.random.choice(list('abcdefghijklmnopqrstuvwxyz '))
                
                # Generate dwell time
                dwell = np.random.normal(params['dwell_mean'], params['dwell_std'])
                dwell = max(0.02, dwell)  # Minimum 20ms
                
                # Record keystroke
                keystrokes.append({
                    'key': key,
                    'press_time': round(current_time, 4),
                    'release_time': round(current_time + dwell, 4)
                })
                
                # Generate flight time to next key
                flight = np.random.normal(params['flight_mean'], params['flight_std'])
                flight = max(0.01, flight)
                current_time += dwell + flight
            
            all_data.append({
                'id': f"{emotion}_{sample_id}",
                'emotion': emotion,
                'keystrokes': keystrokes,
                'timestamp': f"2024-01-{np.random.randint(1, 28):02d}"
            })
    
    # Shuffle data
    np.random.shuffle(all_data)
    
    # Save to JSON
    with open(save_path, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"Generated {len(all_data)} samples")
    print(f"Saved to {save_path}")
    
    return all_data