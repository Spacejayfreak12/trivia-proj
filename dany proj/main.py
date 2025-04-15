#!/usr/bin/env python3
# Adaptive Trivia Quiz Game - Main Module
import time
import os
import sys

from game_logic import TriviaGame
from data_handler import DataHandler
from ai_module import get_predictor
from utils import (
    clear_screen, print_header, print_centered, print_feedback,
    create_difficulty_label, generate_ascii_progress_bar
)

def welcome_screen():
    """Display the welcome screen and get player information."""
    clear_screen()
    print_header("🎮 AI-ENHANCED ADAPTIVE TRIVIA QUIZ GAME 🎮")
    print("Welcome to the Trivia Quiz Game that adapts to your performance!")
    print("The game will adjust its difficulty based on how well you're doing.\n")
    
    player_name = input("Please enter your name: ").strip()
    if not player_name:
        player_name = "Player"
    
    print(f"\nWelcome, {player_name}! Let's get started.\n")
    print("Game instructions:")
    print(" - Answer each question by typing the number (1-4) of your choice")
    print(" - The faster you answer correctly, the more points you earn")
    print(" - The game will adapt to your performance using AI")
    print(" - After each question, the difficulty will adjust automatically\n")
    
    input("Press Enter to begin the game...")
    return player_name

def display_difficulty_change(old_difficulty, new_difficulty):
    """Display information about difficulty change between rounds."""
    old_label = create_difficulty_label(old_difficulty)
    new_label = create_difficulty_label(new_difficulty)
    
    if abs(new_difficulty - old_difficulty) < 0.05:
        print("\nDifficulty remains at", new_label)
    elif new_difficulty > old_difficulty:
        print(f"\nDifficulty increased: {old_label} → {new_label}")
    else:
        print(f"\nDifficulty decreased: {old_label} → {new_label}")
    
    print(f"Difficulty level: {generate_ascii_progress_bar(new_difficulty, 1.0)}")
    time.sleep(1.5)

def display_game_summary(player_name, score, data_handler):
    """Display a summary of the game performance."""
    clear_screen()
    print_header(f"🏆 GAME SUMMARY FOR {player_name.upper()} 🏆")
    
    summary = data_handler.get_game_summary()
    
    if isinstance(summary, str):
        print(summary)
        return
    
    print(f"Total Rounds Played: {summary['total_rounds']}")
    print(f"Final Score: {score}")
    print(f"Average Accuracy: {summary['avg_accuracy']:.1f}%")
    print(f"Average Reaction Time: {summary['avg_reaction_time']:.2f} seconds")
    print(f"Average Attempts Per Question: {summary['avg_attempts']:.2f}")
    
    # Save data to CSV
    try:
        filepath = data_handler.save_to_csv()
        print(f"\nYour game data has been saved to: {filepath}")
    except Exception as e:
        print(f"\nCould not save game data: {e}")
    
    print("\nThank you for playing the Adaptive Trivia Quiz Game!")

def main():
    """Main function to run the game."""
    # Display welcome screen and get player name
    player_name = welcome_screen()
    
    # Initialize components
    game = TriviaGame(player_name)
    data_handler = DataHandler(player_name)
    ai_predictor = get_predictor()
    
    # Game configuration
    max_rounds = 10
    
    # Main game loop
    try:
        for round_num in range(1, max_rounds + 1):
            # Run a round and get performance data
            round_data = game.run_round()
            
            # Get current game difficulty
            current_difficulty = game.get_current_difficulty()
            
            # Log performance data
            data_handler.log_performance(
                round_num,
                current_difficulty,
                round_data["accuracy"],
                round_data["reaction_time"],
                round_data["attempts"]
            )
            
            # Get performance metrics
            avg_accuracy, avg_reaction_time, avg_attempts = data_handler.get_average_metrics()
            
            # Use AI to predict new difficulty
            new_difficulty = ai_predictor.predict_difficulty(
                avg_accuracy, 
                avg_reaction_time,
                avg_attempts
            )
            
            # Adjust game difficulty
            game.adjust_difficulty(new_difficulty)
            
            # Display difficulty change information
            display_difficulty_change(current_difficulty, new_difficulty)
            
            # Check if this is the last round
            if round_num == max_rounds:
                break
            
            # Ask if player wants to continue
            if round_num % 3 == 0:  # Ask every 3 rounds
                choice = input("\nContinue playing? (y/n): ").lower().strip()
                if choice and choice[0] == 'n':
                    break
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted by player.")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
    
    # Display game summary
    display_game_summary(player_name, game.get_score(), data_handler)

if __name__ == "__main__":
    main() 