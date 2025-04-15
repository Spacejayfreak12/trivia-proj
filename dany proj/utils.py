import time
import random
import os

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def start_timer():
    """Start a timer and return the start time."""
    return time.time()

def get_elapsed_time(start_time):
    """Calculate the elapsed time since start_time."""
    return time.time() - start_time

def format_time(seconds):
    """Format time in seconds to a readable string."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    mins, secs = divmod(seconds, 60)
    return f"{int(mins)}:{secs:.2f}"

def shuffle_list(items):
    """Shuffle a list and return the shuffled version."""
    shuffled = items.copy()
    random.shuffle(shuffled)
    return shuffled

def format_score(score, multiplier=1.0):
    """Format the score with optional multiplier."""
    return f"{score * multiplier:.0f}"

def print_centered(text, width=80, fill_char='='):
    """Print text centered with decorative characters on both sides."""
    if len(text) + 4 >= width:
        print(text)
        return
    
    remaining = width - len(text) - 2
    left = remaining // 2
    right = remaining - left
    
    print(f"{fill_char * left} {text} {fill_char * right}")

def print_header(text, width=80):
    """Print a header with the text centered."""
    print("\n" + "=" * width)
    print_centered(text, width)
    print("=" * width + "\n")

def print_feedback(text, is_positive=True):
    """Print feedback with appropriate formatting."""
    prefix = "✓" if is_positive else "✗"
    print(f"\n{prefix} {text}\n")

def input_with_timeout(prompt, timeout=10):
    """
    Simulate input with a timeout by showing a countdown.
    Note: This is a simple implementation and doesn't actually cut off input.
    For a true timeout input, platform-specific solutions would be needed.
    """
    print(f"{prompt} (You have {timeout} seconds)")
    start = time.time()
    
    for remaining in range(timeout, 0, -1):
        print(f"\rTime remaining: {remaining}s ", end="")
        time.sleep(1)
        if time.time() - start >= timeout:
            print("\rTime's up!            ")
            return None
    
    user_input = input("\nYour answer: ")
    return user_input

def generate_ascii_progress_bar(value, max_value, width=20):
    """Generate an ASCII progress bar."""
    percentage = value / max_value
    filled_length = int(width * percentage)
    bar = '█' * filled_length + '░' * (width - filled_length)
    percentage_display = f"{percentage * 100:.1f}%"
    return f"[{bar}] {percentage_display}"

def create_difficulty_label(difficulty):
    """Convert a difficulty value (0-1) to a readable label."""
    if difficulty <= 0.2:
        return "Very Easy"
    elif difficulty <= 0.4:
        return "Easy"
    elif difficulty <= 0.6:
        return "Medium"
    elif difficulty <= 0.8:
        return "Hard"
    else:
        return "Very Hard" 