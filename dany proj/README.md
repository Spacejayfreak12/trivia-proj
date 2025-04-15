# AI-Enhanced Adaptive Trivia Quiz Game

An intelligent trivia web application that uses a neural network to adapt difficulty levels based on player performance metrics.

## Features

- **Adaptive Difficulty**: Game adjusts questions based on player accuracy, reaction time, and attempts
- **Neural Network Integration**: Uses TensorFlow to create a predictor model for dynamic difficulty adjustment
- **Performance Tracking**: Logs player data and provides performance summaries
- **External Question Bank**: Uses a JSON file for question storage and management
- **Intelligent Question Selection**: Selects questions based on difficulty and avoids repetition
- **Timed Questions**: Challenges players to answer quickly for bonus points
- **Web Interface**: Clean, responsive UI built with Flask and modern HTML/CSS
- **Error Handling**: Gracefully handles invalid inputs and unexpected issues
- **JSON Session Serialization**: Properly manages JSON serialization in Flask sessions for stable state management
- **Persistent Public URL**: Creates a consistent, shareable public URL using pyngrok with a reserved subdomain

## Requirements

- Python 3.6 or higher
- Dependencies listed in `requirements.txt`
- ngrok account (for persistent subdomain)

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application Locally

You can run the application in two ways:

### Option 1: Run with Python directly

```bash
python app.py
```

### Option 2: Use Flask's built-in command

```bash
export FLASK_APP=app.py
flask run
```

By default, the web application will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

You can change the port by setting the `PORT` environment variable:

```bash
# On Linux/MacOS
export PORT=8080
python app.py

# On Windows
set PORT=8080
python app.py
```

**Note for macOS users**: Port 5000 may be used by AirPlay. If you encounter issues, modify the port using the method above or append the port flag:

```bash
flask run --port=8080
```

## Setting Up a Persistent Public URL

The application now supports creating a persistent public URL with a consistent subdomain, allowing you to share the same link every time you run the application.

### Step 1: Create an ngrok Account

1. Sign up for a free account at [ngrok.com](https://ngrok.com/signup)
2. Verify your email and log in to your dashboard
3. Navigate to the "Getting Started" section to find your authtoken

### Step 2: Reserve a Subdomain

1. If you have a paid ngrok account, you can reserve a custom subdomain:
   - Go to the [ngrok dashboard](https://dashboard.ngrok.com)
   - Navigate to "Domains" in the left sidebar
   - Click "New Domain" and follow the instructions to register your subdomain

2. If you're using a free account, you won't be able to reserve a permanent subdomain, but you can still use the temporary URL generation feature.

### Step 3: Set Environment Variables

Set the following environment variables before running the application:

```bash
# On Linux/MacOS
export NGROK_AUTHTOKEN=your_authtoken_here
export NGROK_SUBDOMAIN=your_reserved_subdomain
export PORT=5000  # Optional, default is 5000

# On Windows
set NGROK_AUTHTOKEN=your_authtoken_here
set NGROK_SUBDOMAIN=your_reserved_subdomain
set PORT=5000  # Optional, default is 5000
```

You can also add these to your shell's profile or create a script to set them automatically.

### Step 4: Run the Application

```bash
python app.py
```

The application will:
1. Authenticate with ngrok using your authtoken
2. Create a tunnel using your reserved subdomain
3. Display the persistent public URL in the console:
   ```
   * Persistent Public URL: https://your-subdomain.ngrok.io
   * Share this URL with others to let them access your trivia game!
   ```

### Using the Convenience Scripts

For an easier way to run the application with environment variables, you can use the included convenience scripts:

#### On Linux/MacOS:
```bash
# Make the script executable
chmod +x run_app.sh

# Run with your authtoken and subdomain
./run_app.sh -a your_authtoken_here -s your_subdomain -p 5000
```

#### On Windows:
```cmd
run_app.bat -a your_authtoken_here -s your_subdomain -p 5000
```

These scripts will set the environment variables for you and then run the application.

### Fallback to Temporary URL

If you run the application without setting the environment variables `NGROK_AUTHTOKEN` and `NGROK_SUBDOMAIN`, it will fall back to creating a temporary public URL that will change each time you restart the application.

## Sharing Your Application Externally

The application provides multiple options for sharing it externally:

### Option 1: Persistent Public URL (Recommended)

For a consistent link that doesn't change between app restarts:

1. Follow the "Setting Up a Persistent Public URL" instructions above
2. Use the displayed persistent URL to share your application:
   ```
   * Persistent Public URL: https://your-subdomain.ngrok.io
   ```

### Option 2: Temporary Public URL

If you don't need a persistent subdomain:

1. Make sure pyngrok is installed
2. Run the application without setting the environment variables:
   ```bash
   python app.py
   ```
3. The app will create a temporary public URL:
   ```
   * Temporary Public URL: https://abc123.ngrok.io
   * Note: This URL will change each time you restart the app.
   ```

### Option 3: Local Network Sharing

1. Find your computer's local IP address:
   - On Windows: Open Command Prompt and type `ipconfig`
   - On macOS/Linux: Open Terminal and type `ifconfig` or `ip addr`

2. Run the application:
   ```bash
   python app.py
   ```

3. Share your application with others on the same network using your IP address:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

## Troubleshooting Public URL Generation

If you encounter issues with the public URL generation:

1. **ngrok authentication errors**: Verify that your authtoken is correct and properly set as an environment variable.

2. **Subdomain already in use**: If you see an error like "failed to start tunnel: the tunnel 'your-subdomain' is already registered", try the following:
   - Make sure no other instances of your app are running
   - Try a different subdomain
   - Wait a few minutes, as ngrok may take time to release the subdomain

3. **Port conflicts**: If you see "Port X is already in use", set a different port with the PORT environment variable.

4. **Paid plan required**: Some features like custom subdomains require a paid ngrok plan. Check your account status if you encounter limitations.

5. **Firewall issues**: Ensure your firewall allows outbound connections to ngrok's servers.

## How to Play

1. Enter your name on the home page to begin
2. Each question has a 15-second timer (shown by a progress bar)
3. Select your answer by clicking one of the options
4. After each answer, the AI will analyze your performance and adjust the difficulty
5. At the end of the game, you'll see your final score and performance statistics

## Project Structure

- `app.py`: Flask application with routes for the web interface
- `game_logic.py`: Core game mechanics and trivia question logic
- `ai_module.py`: AI/neural network implementation for difficulty prediction
- `data_handler.py`: Handles performance data logging and analysis
- `utils.py`: Helper functions for timing, display, etc.
- `question_bank.json`: External JSON file containing trivia questions with difficulty levels
- `templates/`: HTML templates for the web interface
  - `index.html`: Home/login page
  - `game.html`: Game interface with questions
  - `results.html`: Results and performance summary page
- `tests.py`: Comprehensive unit tests for all components

## Question Bank Format

The `question_bank.json` file follows this structure:

```json
[
    {
        "id": 1,
        "text": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": 0,
        "difficulty": "easy"
    },
    ...
]
```

- `id`: Unique identifier for the question
- `text`: The question text
- `options`: Array of answer options
- `answer`: Index of the correct answer (0-based)
- `difficulty`: Difficulty level ("easy", "medium", or "hard")

## Key Implementations

### Question Selection Logic

The game selects questions based on the current difficulty level and ensures that questions aren't repeated within a session. If no suitable questions are available at the current difficulty level, the selection criteria are relaxed. If all questions have been asked, the asked_questions set is cleared to allow for reusing questions.

### JSON Serialization

The application carefully handles JSON serialization in Flask sessions by converting non-serializable data types (like sets) to appropriate serializable types (like lists) before storing them in the session.

```python
# Before storing in session:
session['asked_questions'] = list(asked_questions)

# When retrieving from session:
asked_questions = set(session.get('asked_questions', []))
```

### AI Integration

The neural network model continuously analyzes player performance metrics (accuracy, reaction time, attempts) and dynamically adjusts the difficulty level for each subsequent question.

### Persistent Public URL

The application uses pyngrok to create a consistent, shareable public URL with your own reserved subdomain. This allows you to share the same link every time you run the application, making it easier to distribute to friends, testers, or reviewers.

## Fallback Support

The game includes a fallback mechanism if TensorFlow is not available, using a simpler rule-based system for difficulty adjustment.

Similarly, if the persistent URL can't be created (e.g., missing environment variables), the application falls back to creating a temporary URL or providing instructions for manual sharing.

## Extending the Game

To add more questions, edit the `question_bank.json` file following the existing question format. 

## Running Tests

To run the unit tests:

```bash
python -m unittest tests.py
```

Or to run specific test classes:

```bash
python -m unittest tests.TestAIModule
``` 