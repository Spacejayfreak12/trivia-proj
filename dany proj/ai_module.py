import numpy as np
import os
import pickle

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    print("TensorFlow not available. Using fallback prediction mechanism.")
    TF_AVAILABLE = False

class DifficultyPredictor:
    def __init__(self, model_path=None):
        """Initialize the difficulty predictor."""
        self.model = None
        self.tf_available = TF_AVAILABLE
        
        if self.tf_available:
            if model_path and os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
            else:
                self.model = self.create_model()
                self.train_on_simulated_data()
        else:
            # Fallback for systems without TensorFlow
            self.fallback_model = self.load_fallback_model(model_path)
    
    def create_model(self):
        """Create and compile the neural network model."""
        if not self.tf_available:
            return None
            
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(16, activation='relu', input_shape=(3,)),
            tf.keras.layers.Dense(8, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model
    
    def train_on_simulated_data(self, n_samples=1000):
        """Train the model on simulated data."""
        if not self.tf_available or self.model is None:
            return False
            
        # Generate synthetic training data
        np.random.seed(42)  # For reproducibility
        
        # Simulated player performance metrics
        # Format: [accuracy, reaction_time, attempts]
        X = np.random.rand(n_samples, 3)
        X[:, 1] = X[:, 1] * 20  # Scale reaction time to 0-20 seconds
        X[:, 2] = np.floor(X[:, 2] * 3) + 1  # 1-3 attempts
        
        # Difficulty should:
        # - Increase when accuracy is high, reaction time is low, attempts are low
        # - Decrease when accuracy is low, reaction time is high, attempts are high
        # This is a synthetic formula to generate reasonable difficulty levels
        Y = (0.7 * X[:, 0] - 0.2 * (X[:, 1] / 20) - 0.1 * (X[:, 2] / 3))
        # Clip to 0-1 range and reshape
        Y = np.clip(Y, 0.1, 0.9).reshape(-1, 1)
        
        # Train model
        self.model.fit(X, Y, epochs=50, batch_size=32, verbose=0)
        return True
    
    def load_fallback_model(self, model_path=None):
        """Load a fallback model or create a simple rule-based one."""
        # If a pickle file with weights exists, load it
        if model_path and os.path.exists(model_path) and model_path.endswith('.pkl'):
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        
        # Otherwise, return a simple function for rule-based difficulty adjustment
        return lambda accuracy, reaction_time, attempts: min(max(
            accuracy * 1.2 - (reaction_time / 20) * 0.3 - (attempts / 3) * 0.1,
            0.1), 0.9)
    
    def predict_difficulty(self, accuracy, reaction_time, attempts):
        """Predict the next difficulty level based on performance metrics."""
        # Normalize inputs to expected ranges
        norm_reaction_time = min(reaction_time, 20) / 20  # 0-20 seconds scaled to 0-1
        norm_attempts = min(attempts, 3) / 3  # 1-3 attempts scaled to 0-1
        
        input_data = np.array([[accuracy, norm_reaction_time, norm_attempts]])
        
        if self.tf_available and self.model is not None:
            prediction = self.model.predict(input_data, verbose=0)
            difficulty = float(prediction[0][0])
        else:
            difficulty = self.fallback_model(accuracy, norm_reaction_time, norm_attempts)
        
        # Ensure the difficulty stays in range [0.1, 0.9]
        return min(max(difficulty, 0.1), 0.9)
    
    def save_model(self, path='models/difficulty_predictor'):
        """Save the model to disk."""
        if not os.path.exists('models'):
            os.makedirs('models')
            
        if self.tf_available and self.model is not None:
            self.model.save(path)
            return True
        elif not self.tf_available and self.fallback_model is not None:
            with open(path + '.pkl', 'wb') as f:
                pickle.dump(self.fallback_model, f)
            return True
        return False

def get_predictor(model_path=None):
    """Factory function to get a DifficultyPredictor instance."""
    return DifficultyPredictor(model_path) 