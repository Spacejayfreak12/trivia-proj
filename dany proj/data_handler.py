import pandas as pd
import os
from datetime import datetime

class DataHandler:
    def __init__(self, player_name):
        """Initialize the data handler with a player name."""
        self.player_name = player_name
        self.columns = ['round', 'difficulty', 'accuracy', 'reaction_time', 'attempts', 'timestamp']
        self.performance_data = pd.DataFrame(columns=self.columns)
        
    def log_performance(self, round_num, difficulty, accuracy, reaction_time, attempts):
        """Log the performance data for a round."""
        new_data = {
            'round': round_num,
            'difficulty': difficulty,
            'accuracy': accuracy,
            'reaction_time': reaction_time,
            'attempts': attempts,
            'timestamp': datetime.now()
        }
        
        self.performance_data = pd.concat([self.performance_data, 
                                          pd.DataFrame([new_data], 
                                                      columns=self.columns)], 
                                          ignore_index=True)
        return new_data
    
    def get_recent_data(self, n_rounds=3):
        """Get performance data from the most recent n rounds."""
        return self.performance_data.tail(n_rounds)
    
    def get_average_metrics(self, n_rounds=3):
        """Calculate average metrics from the most recent n rounds."""
        recent_data = self.get_recent_data(n_rounds)
        if len(recent_data) == 0:
            return 0.5, 10.0, 1.0  # Default values if no data
        
        avg_accuracy = recent_data['accuracy'].mean()
        avg_reaction_time = recent_data['reaction_time'].mean()
        avg_attempts = recent_data['attempts'].mean()
        
        return avg_accuracy, avg_reaction_time, avg_attempts
    
    def save_to_csv(self, filename=None):
        """Save the performance data to a CSV file."""
        if filename is None:
            filename = f"{self.player_name}_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Create a data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        self.performance_data.to_csv(filepath, index=False)
        return filepath
    
    def get_game_summary(self):
        """Generate a summary of the game performance."""
        if len(self.performance_data) == 0:
            return "No game data available."
        
        total_rounds = len(self.performance_data)
        avg_accuracy = self.performance_data['accuracy'].mean() * 100
        avg_reaction_time = self.performance_data['reaction_time'].mean()
        avg_attempts = self.performance_data['attempts'].mean()
        
        summary = {
            'total_rounds': total_rounds,
            'avg_accuracy': avg_accuracy,
            'avg_reaction_time': avg_reaction_time,
            'avg_attempts': avg_attempts
        }
        
        return summary 