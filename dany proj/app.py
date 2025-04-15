#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import time
import json
import sys
from datetime import datetime

from game_logic import TriviaGame
from data_handler import DataHandler
from ai_module import get_predictor
from utils import create_difficulty_label, generate_ascii_progress_bar

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'

# Global variables to store game state
games = {}  # Dictionary to store game instances by session ID
data_handlers = {}  # Dictionary to store data handlers by session ID
ai_predictors = {}  # Dictionary to store AI predictors by session ID

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page with player registration form."""
    if request.method == 'POST':
        player_name = request.form.get('player_name', '').strip()
        if not player_name:
            flash('Please enter your name to start the game.', 'error')
            return redirect(url_for('index'))

        # Initialize game components
        session['player_name'] = player_name
        session['session_id'] = os.urandom(8).hex()
        session_id = session['session_id']
        
        games[session_id] = TriviaGame(player_name)
        data_handlers[session_id] = DataHandler(player_name)
        ai_predictors[session_id] = get_predictor()
        
        # Initialize game state
        session['round_number'] = 0
        session['max_rounds'] = 10
        session['score'] = 0
        session['start_time'] = time.time()
        
        # Initialize asked_questions as a list (for JSON serialization)
        # Explicitly converting to list for JSON serialization
        session['asked_questions'] = []
        
        return redirect(url_for('game'))
    
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    """Game page with trivia questions and answer form."""
    if 'player_name' not in session or 'session_id' not in session:
        flash('Please enter your name to start the game.', 'error')
        return redirect(url_for('index'))
    
    session_id = session['session_id']
    
    if session_id not in games:
        flash('Your game session expired. Please start a new game.', 'error')
        return redirect(url_for('index'))
    
    game = games[session_id]
    data_handler = data_handlers[session_id]
    ai_predictor = ai_predictors[session_id]
    
    # Update asked_questions in the game instance from session
    # Explicitly converting from list to set for the game logic
    if 'asked_questions' in session:
        game.set_asked_questions(session['asked_questions'])
    
    # Process answer if POST request
    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip()
        reaction_time = time.time() - session.get('question_time', time.time())
        question_id = int(request.form.get('question_id', -1))
        
        # Get the current question from session
        current_question = session.get('current_question', None)
        
        if current_question and question_id == current_question.get('id', -2):
            # Evaluate answer
            correct, points = game.evaluate_answer(current_question, user_answer, reaction_time)
            
            # Update game state
            round_result = {
                "correct": correct,
                "points": points,
                "reaction_time": reaction_time,
                "attempts": 1,  # Simplified for web version
                "accuracy": 1.0 if correct else 0.0,
                "difficulty": current_question['difficulty']
            }
            
            # Update score in both game instance and session
            game.update_score(points)
            session['score'] = game.get_score()
            
            # Get current game difficulty
            current_difficulty = game.get_current_difficulty()
            
            # Log performance data
            data_handler.log_performance(
                session['round_number'],
                current_difficulty,
                round_result["accuracy"],
                round_result["reaction_time"],
                round_result["attempts"]
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
            
            # Store feedback in session (ensure all values are JSON serializable)
            session['feedback'] = {
                'correct': correct,
                'points': points,
                'old_difficulty': create_difficulty_label(current_difficulty),
                'new_difficulty': create_difficulty_label(new_difficulty),
                'difficulty_change': "increase" if new_difficulty > current_difficulty else "decrease",
                'progress_bar': generate_ascii_progress_bar(new_difficulty, 1.0)
            }
            
            # Update asked_questions in session from game instance
            # Explicitly converting from set to list for JSON serialization
            session['asked_questions'] = game.get_asked_questions()
            
            # Increment round number
            session['round_number'] += 1
            
            # Check if game is over
            if session['round_number'] >= session['max_rounds']:
                return redirect(url_for('results'))
            
            # Redirect to avoid form resubmission
            return redirect(url_for('game'))
    
    # Generate a new question
    session['round_number'] = session.get('round_number', 0) + (1 if request.method == 'GET' and session.get('round_number', 0) == 0 else 0)
    current_round = session['round_number']
    
    if current_round > session['max_rounds']:
        return redirect(url_for('results'))
    
    # Generate question with unique ID to prevent duplicate submissions
    question = game.generate_question()
    
    # Ensure the question has an ID
    if 'id' not in question:
        question['id'] = int(time.time())  # Use timestamp as unique ID
    
    # Store question and start time in session
    session['current_question'] = question
    session['question_time'] = time.time()
    
    # Update asked_questions in session
    # Explicitly converting from set to list for JSON serialization
    session['asked_questions'] = game.get_asked_questions()
    
    # Get feedback from previous round
    feedback = session.pop('feedback', None)
    
    # Process the difficulty change display
    difficulty_change = None
    if feedback and 'difficulty_change' in feedback:
        if feedback['difficulty_change'] == "increase":
            difficulty_change = True
        elif feedback['difficulty_change'] == "decrease":
            difficulty_change = False
    
    if feedback:
        feedback['difficulty_change'] = difficulty_change
    
    return render_template(
        'game.html',
        player_name=session['player_name'],
        round_number=current_round,
        max_rounds=session['max_rounds'],
        question=question,
        score=session.get('score', 0),
        feedback=feedback,
        difficulty=create_difficulty_label(game.get_current_difficulty())
    )

@app.route('/results')
def results():
    """Results page with final score and performance summary."""
    if 'player_name' not in session or 'session_id' not in session:
        flash('Please enter your name to start the game.', 'error')
        return redirect(url_for('index'))
    
    session_id = session['session_id']
    
    if session_id not in games or session_id not in data_handlers:
        flash('Your game session expired. Please start a new game.', 'error')
        return redirect(url_for('index'))
    
    player_name = session['player_name']
    game = games[session_id]
    data_handler = data_handlers[session_id]
    
    # Get game summary
    summary = data_handler.get_game_summary()
    score = game.get_score()
    
    # Save data to CSV
    try:
        filepath = data_handler.save_to_csv()
        csv_saved = True
        csv_path = filepath
    except Exception as e:
        print(f"Error saving CSV: {e}")
        csv_saved = False
        csv_path = None
    
    # Calculate total time played
    total_time = time.time() - session.get('start_time', time.time())
    total_time_str = f"{int(total_time // 60)} minutes and {int(total_time % 60)} seconds"
    
    # Get statistics on question difficulty distribution
    question_stats = {
        'total_questions': len(session.get('asked_questions', [])),
        'easy_questions': 0,
        'medium_questions': 0,
        'hard_questions': 0
    }
    
    # Clean up game resources
    if session_id in games:
        del games[session_id]
    if session_id in data_handlers:
        del data_handlers[session_id]
    if session_id in ai_predictors:
        del ai_predictors[session_id]
    
    return render_template(
        'results.html',
        player_name=player_name,
        score=score,
        rounds_played=summary['total_rounds'] if isinstance(summary, dict) else 0,
        avg_accuracy=f"{summary['avg_accuracy']:.1f}%" if isinstance(summary, dict) else "N/A",
        avg_reaction_time=f"{summary['avg_reaction_time']:.2f} seconds" if isinstance(summary, dict) else "N/A",
        avg_attempts=f"{summary['avg_attempts']:.2f}" if isinstance(summary, dict) else "N/A",
        total_time=total_time_str,
        csv_saved=csv_saved,
        csv_path=csv_path,
        question_stats=question_stats
    )

@app.route('/restart')
def restart():
    """Restart the game by clearing the session."""
    session_id = session.get('session_id')
    
    # Clean up game resources
    if session_id in games:
        del games[session_id]
    if session_id in data_handlers:
        del data_handlers[session_id]
    if session_id in ai_predictors:
        del ai_predictors[session_id]
    
    # Clear session
    session.clear()
    
    return redirect(url_for('index'))

@app.route('/api/question-stats')
def question_stats():
    """API endpoint to get question statistics."""
    if 'session_id' not in session:
        return jsonify({'error': 'No active session'}), 400
        
    questions_asked = len(session.get('asked_questions', []))
    
    return jsonify({
        'questions_asked': questions_asked,
        'max_questions': session.get('max_rounds', 10)
    })

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Determine the port from the environment, default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Setup pyngrok for a persistent public URL using a reserved subdomain
    try:
        from pyngrok import ngrok
        authtoken = os.environ.get('NGROK_AUTHTOKEN')
        subdomain = os.environ.get('NGROK_SUBDOMAIN')
        
        if authtoken and subdomain:
            ngrok.set_auth_token(authtoken)
            public_url = ngrok.connect(port, subdomain=subdomain)
            print(" * Persistent Public URL:", public_url)
            print(" * Share this URL with others to let them access your trivia game!")
        else:
            print(" * NGROK_AUTHTOKEN and NGROK_SUBDOMAIN not set.")
            print(" * To get a persistent URL, sign up for ngrok, reserve a subdomain,")
            print(" * and set these environment variables.")
            
            # Try to create a temporary public URL without a reserved subdomain
            try:
                temp_url = ngrok.connect(port)
                print(" * Temporary Public URL:", temp_url)
                print(" * Note: This URL will change each time you restart the app.")
            except Exception as e:
                print(f" * Error creating temporary URL: {e}")
    except ImportError:
        print("pyngrok is not installed. Please run 'pip install pyngrok' and try again.")
    except Exception as e:
        print(f"Error setting up ngrok: {e}")
    
    # Run the Flask app, binding to 0.0.0.0 so it's accessible externally
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except OSError as e:
        print(f"Error: {e}")
        print("Port", port, "is in use. Please set a different port with the PORT environment variable.") 