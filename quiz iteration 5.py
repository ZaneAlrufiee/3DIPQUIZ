import random  # Importing the random module to shuffle questions for each quiz session
import time  # Importing the time module to manage the timing for questions and quizzes
from datetime import datetime  # Importing datetime for any future date/time needs
import easygui  # Importing easygui to create user-friendly graphical interfaces
from question_bank_2 import questions_by_subject  # Importing the question bank, organized by subject

leaderboard_file = "leaderboard_scores.txt"  # File to keep track of the top scores for the leaderboard


class Leaderboard:
    def __init__(self):
        self.scores = []  # Initialize an empty list to store the top 10 scores
        self.load_leaderboard()  # Load existing scores from the file when creating the leaderboard

    def load_leaderboard(self):
        """Loads the leaderboard from the file and handles different formats."""
        try:
            with open(leaderboard_file, 'r') as file:  # Try to open the leaderboard file
                for line in file:  # Read each line in the file
                    parts = line.strip().split(', ')  # Split the line into components
                    if len(parts) == 4:  # New format with name, score, difficulty, and subject
                        name, score, difficulty, subject = parts
                    elif len(parts) == 2:  # Old format with just name and score
                        name, score = parts
                        difficulty = "N/A"  # No difficulty available in old format
                        subject = "N/A"  # No subject available in old format
                    else:
                        continue  # Skip any lines that don't match expected formats
                    self.scores.append((int(score), name, difficulty, subject))  # Add scores to the list
        except FileNotFoundError:
            pass  # If the file doesn't exist, just start with an empty leaderboard

    def save_leaderboard(self):
        """Saves the leaderboard to the file."""
        with open(leaderboard_file, 'w') as file:  # Open the file for writing
            for score, name, difficulty, subject in self.scores:  # Loop through the scores
                file.write(f"{name}, {score}, {difficulty}, {subject}\n")  # Write each score to the file

    def update_leaderboard(self, name, score, difficulty, subject):
        """Updates the leaderboard with a new score, ensuring only the top 10 are kept."""
        self.scores.append((score, name, difficulty, subject))  # Add a new score to the leaderboard
        self.scores.sort(reverse=True, key=lambda x: x[0])  # Sort scores from highest to lowest
        self.scores = self.scores[:10]  # Keep only the top 10 scores
        self.save_leaderboard()  # Save the updated leaderboard to the file

    def show_leaderboard(self):
        """Displays the leaderboard to the user."""
        if not self.scores:  # Check if there are no scores recorded yet
            easygui.msgbox("No scores recorded yet.", title="Leaderboard", image="leaderboard.gif")  # Show a message
        else:
            # Create a formatted string of the top scores for display
            leaderboard_text = "\n".join([f"{i + 1}. {name} - {score} (Difficulty: {difficulty}, Subject: {subject})"
                                          for i, (score, name, difficulty, subject) in enumerate(self.scores)])
            easygui.msgbox(f"Top 10 Scores:\n\n{leaderboard_text}", title="Leaderboard", image="leaderboard.gif")  # Show the leaderboard


class Quiz:
    def __init__(self):
        """Initializes the Quiz class with a leaderboard and total score."""
        self.leaderboard = Leaderboard()  # Create a leaderboard instance to keep track of scores
        self.total_score = 0  # Initialize the total score for the user

    def show_welcome_screen(self):
        """Displays a welcome screen with a friendly message."""
        welcome_message = (
            "Welcome to my general knowledge quiz!\n\n"
            "In this quiz, you can choose from a variety of subjects and difficulty levels.\n"
            "You can take a quiz in Easy, Medium, or Hard difficulty, and a maximum of 10 questions.\n"
            "You also have the option to take the quiz in timed mode or regular mode.\n\n"
            "Good luck and have fun!"
        )
        easygui.msgbox(welcome_message, title="Welcome", image="./images/welcome_image.png")  # Show the welcome message

    def get_user_details(self):
        """Prompts the user to enter their name and age, ensuring they are eligible for the quiz."""
        name = easygui.enterbox("Enter your name:", title="Quiz Login")  # Prompt for the user's name
        if name is None:
            return None  # Exit if the user closes the dialog

        # Prompt for age and verify eligibility
        age = easygui.integerbox("Enter your age:", title="Quiz Age Verification", lowerbound=0, upperbound=120)
        if age is None or age <= 9:  # Check if age is valid
            easygui.msgbox("Sorry, you are ineligible for the quiz due to age restrictions.", title="Ineligible")  # Inform if ineligible
            return None
        else:
            easygui.msgbox(f"Welcome, {name}! You are eligible for the quiz.", title="Welcome")  # Welcome eligible users

        # Prompt for year level
        year_level = easygui.enterbox("Enter your year level:", title="Year Level")
        if year_level is None:
            return None  # Exit if the user closes the dialog

        return name, age, year_level  # Return user details for later use

    def select_subject(self):
        """Allows the user to select a subject for the quiz."""
        subjects = list(questions_by_subject.keys())  # Get the list of available subjects
        subject = easygui.choicebox("Available subjects are:", title="Select Subject", choices=subjects)  # Prompt to select a subject
        return subject  # Return the selected subject

    def select_difficulty(self):
        """Prompts the user to select a difficulty level for the quiz."""
        difficulties = ["Easy", "Medium", "Hard"]  # Define available difficulty levels
        difficulty = easygui.choicebox("Select difficulty level:", title="Select Difficulty", choices=difficulties)  # Prompt to select difficulty
        return difficulty  # Return the selected difficulty

    def ask_question(self, question, choices, answer, time_limit=None):
        """Presents a question to the user and checks their answer."""
        start_time = time.time()  # Start timing the question

        while True:  # Keep asking until the user answers or decides to exit
            # Calculate remaining time if a time limit is set
            remaining_time = time_limit - int(time.time() - start_time) if time_limit else None
            
            # If time runs out, notify the user
            if time_limit and remaining_time <= 0:  
                easygui.msgbox("Time's up! Moving to the next question.", title="Time Limit Exceeded")  
                return False  # Move to the next question automatically

            # Show the question and choices to the user
            user_response = easygui.buttonbox(
                f"{question}\n\n{'Time remaining: ' + str(remaining_time) + ' seconds' if remaining_time else ''}",
                title="Quiz Question",
                choices=[f"{chr(97 + i)}. {choices[i]}" for i in range(len(choices))] + ["Exit Quiz"]
            )  
            
            # Handle user wanting to exit the quiz
            if user_response == "Exit Quiz":
                if easygui.ynbox("Are you sure you want to exit the quiz?", title="Exit Confirmation", choices=["Yes", "No"]):
                    return "exit"  # Exit the quiz if confirmed
            elif user_response:  # If the user selects an answer
                # Determine the correct response for feedback
                correct_response = f"{answer}. {choices[ord(answer) - ord('a')]}"  
                if user_response == correct_response:  # Check if the answer is correct
                    easygui.msgbox("Correct!", title="Result")  # Inform the user of the correct answer
                    return True  # Return true for a correct answer
                else:
                    easygui.msgbox(f"Incorrect. The correct answer was: {correct_response}", title="Result")  # Show the correct answer
                    return False  # Return false for an incorrect answer

    def quiz_on_subject(self, subject, difficulty, total_questions, quiz_time_limit=None):
        """Conducts the quiz on the selected subject and difficulty level."""
        # Filter questions by subject and difficulty, then shuffle for randomness
        questions = [q for q in questions_by_subject[subject] if q[3] == difficulty.lower()]  
        random.shuffle(questions)  # Shuffle questions for randomness
        score = 0  # Initialize score for this quiz
        start_time = time.time()  # Start timing the quiz

        for i, (question, choices, answer, _) in enumerate(questions[:total_questions]):  # Loop through the questions
            if quiz_time_limit:  # Check if a time limit is set for the whole quiz
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                remaining_quiz_time = quiz_time_limit - elapsed_time  # Calculate remaining time
                if remaining_quiz_time <= 0:  # If the time runs out
                    easygui.msgbox("Time's up! You've completed the quiz.", title="Quiz Over")  
                    break  # End the quiz

            # Ask each question and get feedback
            result = self.ask_question(question, choices, answer, time_limit=15)  # Set time limit for each question
            if result == "exit":  # Check if the user chose to exit
                return  # Exit if requested
            if result:  # If the answer was correct
                score += 1  # Increase the score for a correct answer

        # Show the final score and update leaderboard
        easygui.msgbox(f"You scored {score}/{total_questions} questions correct!", title="Quiz Finished")  
        self.leaderboard.update_leaderboard(self.user_name, score, difficulty, subject)  # Update leaderboard with score

    def start_quiz(self):
        """Manages the overall flow of the quiz."""
        self.show_welcome_screen()  # Show the welcome screen
        user_details = self.get_user_details()  # Get user details
        if user_details is None:  # Check for eligibility
            return  # Exit if not eligible

        self.user_name, age, year_level = user_details  # Unpack user details

        while True:  # Keep prompting for quizzes until the user chooses to exit
            subject = self.select_subject()  # Select subject for the quiz
            difficulty = self.select_difficulty()  # Select difficulty for the quiz

            total_questions = easygui.integerbox("Enter the number of questions (1-10):", title="Question Count", lowerbound=1, upperbound=10)  # Get number of questions
            if total_questions is None:
                return  # Exit if cancelled

            # Ask the user if they want a timed quiz
            timed_quiz = easygui.ynbox("Do you want to set a time limit for the quiz?", title="Timed Quiz Option")  
            quiz_time_limit = None  # Initialize time limit
            if timed_quiz:
                quiz_time_limit = easygui.integerbox("Enter the time limit in seconds:", title="Time Limit", lowerbound=1)  # Get time limit

            # Start the quiz with selected parameters
            self.quiz_on_subject(subject, difficulty, total_questions, quiz_time_limit)  

            # Ask if the user wants to take another quiz
            if not easygui.ynbox("Would you like to take another quiz?", title="Another Quiz"):
                break  # Exit if they don't want to take another quiz

        self.leaderboard.show_leaderboard()  # Show the leaderboard at the end of the session


# Main execution point
if __name__ == "__main__":
    quiz = Quiz()  # Create a Quiz instance
    quiz.start_quiz()  # Start the quiz process
