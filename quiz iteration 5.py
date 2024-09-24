import easygui
import random
import time
from datetime import datetime
from question_bank_2 import questions_by_subject  # Import the question bank

leaderboard_file = "leaderboard_scores.txt"  # File to store leaderboard scores
leaderboard = []  # Stores the top 10 scores

def load_leaderboard():
    """Loads the leaderboard from the file and handles different formats."""
    try:
        with open(leaderboard_file, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) == 4:
                    name, score, difficulty, subject = parts
                elif len(parts) == 2:  # Handle old format
                    name, score = parts
                    difficulty = "N/A"
                    subject = "N/A"
                else:
                    continue  # Skip any malformed lines
                leaderboard.append((int(score), name, difficulty, subject))
    except FileNotFoundError:
        pass  # If the file doesn't exist, start with an empty leaderboard

def save_leaderboard():
    """Saves the leaderboard to the file."""
    with open(leaderboard_file, 'w') as file:
        for score, name, difficulty, subject in leaderboard:
            file.write(f"{name}, {score}, {difficulty}, {subject}\n")

def show_welcome_screen():
    """Displays a welcome screen with a message and an image."""
    welcome_message = (
        "Welcome to my general knowledge quiz!\n\n"
        "In this quiz, you can choose from a variety of subjects and difficulty levels.\n"
        "You can take a quiz in Easy, Medium, or Hard difficulty, and a maximum of 10 questions.\n"
        "You also have the option to take the quiz in timed mode or regular mode.\n\n"
        "Good luck and have fun!"
    )
    easygui.msgbox(welcome_message, title="Welcome", image="welcome_image.png")

def get_user_details():
    name = easygui.enterbox("Enter your name:", title="Quiz Login")
    if name is None:
        return None  # Exit if the user closes the dialog

    age = easygui.integerbox("Enter your age:", title="Quiz Age Verification", lowerbound=0, upperbound=120)
    if age is None or age <= 9:
        easygui.msgbox("Sorry, you are ineligible for the quiz due to age restrictions.", title="Ineligible")
        return None
    else:
        easygui.msgbox(f"Welcome, {name}! You are eligible for the quiz.", title="Welcome")

    year_level = easygui.enterbox("Enter your year level:", title="Year Level")
    if year_level is None:
        return None  # Exit if the user closes the dialog

    return name, age, year_level

def select_subject():
    subjects = list(questions_by_subject.keys())
    subject = easygui.choicebox("Available subjects are:", title="Select Subject", choices=subjects)
    return subject

def select_difficulty():
    difficulties = ["Easy", "Medium", "Hard"]
    difficulty = easygui.choicebox("Select difficulty level:", title="Select Difficulty", choices=difficulties)
    return difficulty

def ask_question(question, choices, answer, time_limit=None):
    start_time = time.time()

    while True:
        remaining_time = time_limit - int(time.time() - start_time) if time_limit else None
        
        if time_limit and remaining_time <= 0:
            easygui.msgbox("Time's up! Moving to the next question.", title="Time Limit Exceeded")
            return False  # Automatically move to the next question

        user_response = easygui.buttonbox(f"{question}\n\n{'Time remaining: ' + str(remaining_time) + ' seconds' if remaining_time else ''}", 
                                          title="Quiz Question", 
                                          choices=[f"{chr(97 + i)}. {choices[i]}" for i in range(len(choices))] + ["Exit Quiz"])
        
        if user_response == "Exit Quiz":
            if easygui.ynbox("Are you sure you want to exit the quiz?", title="Exit Confirmation", choices=["Yes", "No"]):
                return "exit"  # Exit the quiz
        elif user_response:
            correct_response = f"{answer}. {choices[ord(answer) - ord('a')]}"
            if user_response == correct_response:
                easygui.msgbox("Correct!", title="Result")
                return True
            else:
                easygui.msgbox(f"Incorrect. The correct answer was: {correct_response}", title="Result")
                return False

def quiz_on_subject(subject, difficulty, total_questions, quiz_time_limit=None):
    questions = [q for q in questions_by_subject[subject] if q[3] == difficulty.lower()]
    random.shuffle(questions)
    score = 0
    start_time = time.time()

    for i, (question, choices, answer, _) in enumerate(questions[:total_questions]):
        if quiz_time_limit:
            elapsed_time = time.time() - start_time
            if elapsed_time >= quiz_time_limit:
                easygui.msgbox("Time's up for the entire quiz!", title="Time Limit Exceeded")
                break

        result = ask_question(question, choices, answer, time_limit=10 if quiz_time_limit else None)
        if result == "exit":
            return score, True  # Exit the quiz
        elif result:
            score += {"Easy": 1, "Medium": 2, "Hard": 3}[difficulty]

        # Progress Tracking
        progress = int(((i + 1) / total_questions) * 100)
        easygui.msgbox(f"Progress: {progress}% complete", title="Quiz Progress")

    return score, False  # Continue quiz

def update_leaderboard(name, score, difficulty, subject):
    leaderboard.append((score, name, difficulty, subject))
    leaderboard.sort(reverse=True, key=lambda x: x[0])
    leaderboard[:] = leaderboard[:10]  # Keep only top 10 scores
    save_leaderboard()  # Save the updated leaderboard to the file

def show_leaderboard():
    if not leaderboard:
        easygui.msgbox("No scores recorded yet.", title="Leaderboard", image="leaderboard.gif")
    else:
        leaderboard_text = "\n".join([f"{i+1}. {name} - {score} (Difficulty: {difficulty}, Subject: {subject})" 
                                      for i, (score, name, difficulty, subject) in enumerate(leaderboard)])
        easygui.msgbox(f"Top 10 Scores:\n\n{leaderboard_text}", title="Leaderboard", image="leaderboard.gif")

def main():
    show_welcome_screen()  # Display the welcome screen

    load_leaderboard()  # Load the leaderboard from the file at the start

    user_info = get_user_details()
    if user_info is None:
        return  # Exit if the user is ineligible or closes the dialog

    name, age, year_level = user_info

    total_score = 0
    while True:
        subject = select_subject()
        if not subject:
            break  # User cancelled subject selection

        difficulty = select_difficulty()
        if not difficulty:
            break  # User cancelled difficulty selection

        # Ask if they want a timed quiz
        timed_mode = easygui.ynbox("Do you want to play in timed mode?", title="Timed Mode")
        if timed_mode:
            quiz_time_limit = easygui.integerbox("Enter time limit for the entire quiz (in seconds):", title="Quiz Time Limit", lowerbound=30, upperbound=600)
        else:
            quiz_time_limit = None

        # Limit the number of questions to a maximum of 10
        total_questions = easygui.integerbox("How many questions do you want to answer?", title="Question Count", lowerbound=1, upperbound=10)
        
        score, exited = quiz_on_subject(subject, difficulty, total_questions, quiz_time_limit)
        total_score += score
        easygui.msgbox(f"You completed the {subject} quiz on {difficulty} difficulty. Your score is {score}.", title="Quiz Completed")
        
        update_leaderboard(name, total_score, difficulty, subject)  # Update and save the leaderboard with difficulty and subject

        show_leaderboard()  # Display the leaderboard

        if exited or not easygui.ynbox("Would you like to pick another subject?", title="Continue?", choices=["Yes", "No"]):
            easygui.msgbox(f"Thank you, {name}! Your total score is {total_score}.", title="Goodbye")
            break

if __name__ == "__main__":
    main()
