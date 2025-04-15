import random
import time
import json
import os
from utils import start_timer, get_elapsed_time, print_header, print_feedback, input_with_timeout, clear_screen

# Question bank with difficulty levels (0.1: easiest, 0.9: hardest)
QUESTION_BANK = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": 0,
        "difficulty": 0.1
    },
    {
        "question": "Which planet is closest to the Sun?",
        "options": ["Venus", "Mercury", "Earth", "Mars"],
        "answer": 1,
        "difficulty": 0.2
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "answer": 1,
        "difficulty": 0.3
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["H2O", "CO2", "O2", "NaCl"],
        "answer": 0,
        "difficulty": 0.2
    },
    {
        "question": "Which element has the symbol 'Au'?",
        "options": ["Silver", "Aluminum", "Gold", "Copper"],
        "answer": 2,
        "difficulty": 0.4
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "answer": 1,
        "difficulty": 0.3
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1943", "1944", "1945", "1946"],
        "answer": 2,
        "difficulty": 0.4
    },
    {
        "question": "What is the largest organ in the human body?",
        "options": ["Heart", "Brain", "Liver", "Skin"],
        "answer": 3,
        "difficulty": 0.4
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "answer": 2,
        "difficulty": 0.3
    },
    {
        "question": "What is the square root of 144?",
        "options": ["12", "14", "16", "18"],
        "answer": 0,
        "difficulty": 0.3
    },
    # Medium difficulty questions
    {
        "question": "Which scientist developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Stephen Hawking"],
        "answer": 1,
        "difficulty": 0.5
    },
    {
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
        "answer": 2,
        "difficulty": 0.5
    },
    {
        "question": "Which of these elements is a noble gas?",
        "options": ["Chlorine", "Nitrogen", "Argon", "Sodium"],
        "answer": 2,
        "difficulty": 0.6
    },
    {
        "question": "In computing, what does CPU stand for?",
        "options": ["Central Processing Unit", "Computer Personal Unit", "Central Process Utility", "Control Processing Unit"],
        "answer": 0,
        "difficulty": 0.5
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": 3,
        "difficulty": 0.5
    },
    # Hard difficulty questions
    {
        "question": "Which of these is NOT a programming language?",
        "options": ["Java", "Python", "Cobra", "Leopard"],
        "answer": 3,
        "difficulty": 0.7
    },
    {
        "question": "What is the chemical formula for sulfuric acid?",
        "options": ["H2SO3", "H2SO4", "HSO4", "H2S2O7"],
        "answer": 1,
        "difficulty": 0.8
    },
    {
        "question": "What is the half-life of Carbon-14?",
        "options": ["1,570 years", "5,730 years", "10,730 years", "14,500 years"],
        "answer": 1,
        "difficulty": 0.9
    },
    {
        "question": "Who developed the quantum theory?",
        "options": ["Max Planck", "Niels Bohr", "Werner Heisenberg", "Erwin Schrödinger"],
        "answer": 0,
        "difficulty": 0.8
    },
    {
        "question": "In what year was the first transistor invented?",
        "options": ["1945", "1947", "1950", "1954"],
        "answer": 1,
        "difficulty": 0.7
    }
]

def load_question_bank(file_path='question_bank.json'):
    """
    Load questions from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing questions
        
    Returns:
        list: List of question dictionaries
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Question bank file not found: {file_path}")
            
        with open(file_path, 'r') as file:
            questions = json.load(file)
            
        # Validate question format
        for question in questions:
            if not all(key in question for key in ['id', 'text', 'options', 'answer', 'difficulty']):
                raise ValueError(f"Question with ID {question.get('id', 'unknown')} has invalid format")
                
        # Standardize field names if needed
        for question in questions:
            # Convert 'text' to 'question' for consistency
            if 'text' in question and 'question' not in question:
                question['question'] = question['text']
            
        return questions
    except Exception as e:
        print(f"Error loading question bank: {e}")
        # Return a minimal set of questions as fallback
        return _get_default_questions()

def _get_default_questions():
    """
    Return a minimal set of default questions as fallback if loading from JSON fails.
    
    Returns:
        list: List of default question dictionaries
    """
    return [
        {
            "id": 1,
            "text": "What is the capital of France?",
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Madrid"],
            "answer": 0,
            "difficulty": "easy"
        },
        {
            "id": 2,
            "text": "Which scientist developed the theory of relativity?",
            "question": "Which scientist developed the theory of relativity?",
            "options": ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Stephen Hawking"],
            "answer": 1,
            "difficulty": "medium"
        },
        {
            "id": 3,
            "text": "What is the chemical formula for sulfuric acid?",
            "question": "What is the chemical formula for sulfuric acid?",
            "options": ["H2SO3", "H2SO4", "HSO4", "H2S2O7"],
            "answer": 1,
            "difficulty": "hard"
        }
    ]

def convert_difficulty_value_to_label(difficulty_value):
    """
    Convert a numeric difficulty value (0.1-0.9) to a text label (easy, medium, hard).
    
    Args:
        difficulty_value (float): Difficulty value between 0.1 and 0.9
        
    Returns:
        str: Difficulty label ('easy', 'medium', or 'hard')
    """
    if difficulty_value <= 0.3:
        return "easy"
    elif difficulty_value <= 0.6:
        return "medium"
    else:
        return "hard"

def convert_difficulty_label_to_value(difficulty_label):
    """
    Convert a text difficulty label to a numeric value.
    
    Args:
        difficulty_label (str): Difficulty label ('easy', 'medium', or 'hard')
        
    Returns:
        float: Numeric difficulty value
    """
    if difficulty_label == "easy":
        return 0.3
    elif difficulty_label == "medium":
        return 0.6
    else:  # hard
        return 0.9

def select_question(desired_difficulty, asked_questions, question_bank):
    """
    Select a question based on the desired difficulty that hasn't been asked yet.
    
    Args:
        desired_difficulty (str): Desired difficulty level ('easy', 'medium', 'hard')
        asked_questions (set): Set of IDs of questions already asked
        question_bank (list): List of all available questions
        
    Returns:
        dict: Selected question or None if no suitable questions
        bool: Whether the selection constraints were relaxed
    """
    # First, try to find questions with exact difficulty match that haven't been asked
    suitable_questions = [q for q in question_bank 
                         if q['difficulty'] == desired_difficulty 
                         and q['id'] not in asked_questions]
    
    # If no suitable questions with the desired difficulty, relax the difficulty constraint
    constraint_relaxed = False
    if not suitable_questions:
        constraint_relaxed = True
        
        # Try finding any question that hasn't been asked yet
        suitable_questions = [q for q in question_bank if q['id'] not in asked_questions]
        
        # If all questions have been asked or no questions are available at all
        if not suitable_questions and asked_questions:
            # Reset asked_questions if we've gone through all available questions
            if len(asked_questions) >= len([q for q in question_bank if 'id' in q]):
                asked_questions.clear()
                
            # Try again with all questions
            suitable_questions = [q for q in question_bank 
                                if q['difficulty'] == desired_difficulty]
            
            # If still no questions with the desired difficulty, use any question
            if not suitable_questions:
                suitable_questions = question_bank
    
    # Select a random question from suitable ones
    if suitable_questions:
        selected_question = random.choice(suitable_questions)
        # Add to asked_questions set
        if 'id' in selected_question:
            asked_questions.add(selected_question['id'])
        return selected_question, constraint_relaxed
    
    # Fallback to a default question if something went wrong
    if question_bank:
        fallback_question = random.choice(question_bank)
        if 'id' in fallback_question:
            asked_questions.add(fallback_question['id'])
        return fallback_question, True
    else:
        # Create an emergency question if even the question bank is empty
        emergency_question = {
            "id": 999,
            "question": "Emergency fallback question: What is 2+2?",
            "text": "Emergency fallback question: What is 2+2?",
            "options": ["3", "4", "5", "6"],
            "answer": 1,
            "difficulty": desired_difficulty
        }
        return emergency_question, True

class TriviaGame:
    def __init__(self, player_name):
        """Initialize the trivia game."""
        self.player_name = player_name
        self.score = 0
        self.round_number = 0
        self.current_difficulty = 0.5  # Start at medium difficulty
        self.question_bank = load_question_bank()
        self.asked_questions = set()
        
    def generate_question(self, difficulty=None):
        """Generate a question based on the current difficulty level."""
        if difficulty is None:
            difficulty = self.current_difficulty
        
        # Convert numeric difficulty to label
        difficulty_label = convert_difficulty_value_to_label(difficulty)
        
        # Select question
        question, _ = select_question(difficulty_label, self.asked_questions, self.question_bank)
        
        # Convert to the format expected by the web interface
        if 'difficulty' in question and isinstance(question['difficulty'], str):
            # Convert string difficulty to numeric value for consistency
            question['difficulty'] = convert_difficulty_label_to_value(question['difficulty'])
        
        # Ensure both 'text' and 'question' fields exist for template compatibility
        if 'text' in question and 'question' not in question:
            question['question'] = question['text']
        elif 'question' in question and 'text' not in question:
            question['text'] = question['question']
            
        return question
        
    def display_question(self, question_data):
        """Display a question and its options to the player."""
        clear_screen()
        print_header(f"Round {self.round_number} - {self.player_name}'s Trivia Challenge")
        
        print(f"Question: {question_data['question']}\n")
        for i, option in enumerate(question_data['options']):
            print(f"{i+1}. {option}")
        print("\n")
        
    def evaluate_answer(self, question_data, user_answer, time_taken):
        """Evaluate the user's answer."""
        # Convert user input to zero-indexed answer
        try:
            # Handle both numeric and alphabetic input (1, 2, 3, 4 or a, b, c, d)
            if user_answer.isdigit():
                user_choice = int(user_answer) - 1
            elif user_answer.lower() in ['a', 'b', 'c', 'd']:
                user_choice = ord(user_answer.lower()) - ord('a')
            else:
                return False, 0
                
            correct = user_choice == question_data['answer']
            
            # Calculate points based on difficulty and time taken
            points = 0
            if correct:
                # Base points for correct answer (higher difficulty = more points)
                base_points = 100 + int(question_data['difficulty'] * 100)
                
                # Time bonus: faster answers get more points
                time_factor = max(0, 1 - (time_taken / 20))  # 0 to 1, more time = lower factor
                time_bonus = int(base_points * time_factor * 0.5)  # Up to 50% bonus for fast answers
                
                points = base_points + time_bonus
                
            return correct, points
            
        except (ValueError, IndexError):
            return False, 0
    
    def update_score(self, points):
        """Update the player's score."""
        self.score += points
        return self.score
    
    def adjust_difficulty(self, new_difficulty):
        """Adjust the game difficulty based on AI prediction."""
        self.current_difficulty = new_difficulty
        return self.current_difficulty
        
    def run_round(self, timeout=15):
        """Run a complete round of the trivia game."""
        self.round_number += 1
        
        # Generate a question based on current difficulty
        question_data = self.generate_question()
        
        # Display the question
        self.display_question(question_data)
        
        # Start timer for response
        start_time = start_timer()
        
        # Get user's answer with timeout
        answer_timeout = max(5, int(20 - (question_data['difficulty'] * 10)))  # Harder questions get less time
        user_answer = input_with_timeout("Select your answer (1-4):", answer_timeout)
        
        # Calculate reaction time
        reaction_time = get_elapsed_time(start_time)
        
        # If timeout or no answer
        if user_answer is None or user_answer.strip() == "":
            print_feedback("Time's up! No answer provided.", False)
            return {
                "correct": False,
                "points": 0,
                "reaction_time": reaction_time,
                "attempts": 1,
                "accuracy": 0.0,
                "difficulty": question_data['difficulty']
            }
        
        # Evaluate answer
        attempts = 1
        correct, points = self.evaluate_answer(question_data, user_answer, reaction_time)
        
        # Provide feedback
        if correct:
            print_feedback(f"Correct! You earned {points} points.", True)
            self.update_score(points)
        else:
            print_feedback("Incorrect answer.", False)
        
        time.sleep(1.5)  # Brief pause to read feedback
        
        # Return performance data for this round
        return {
            "correct": correct,
            "points": points,
            "reaction_time": reaction_time,
            "attempts": attempts,
            "accuracy": 1.0 if correct else 0.0,
            "difficulty": question_data['difficulty']
        }
    
    def get_score(self):
        """Get the current score."""
        return self.score
        
    def get_current_difficulty(self):
        """Get the current difficulty level."""
        return self.current_difficulty
        
    def get_asked_questions(self):
        """Get the set of asked question IDs (for serialization)."""
        return list(self.asked_questions)
        
    def set_asked_questions(self, asked_questions_list):
        """Set the asked questions from a list (after deserialization)."""
        self.asked_questions = set(asked_questions_list) 