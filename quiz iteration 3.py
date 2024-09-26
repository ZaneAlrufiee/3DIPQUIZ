import easygui  # EasyGUI is a Python library that makes it simple to create dialogs and GUIs for user interaction.
import random  # Random is used to shuffle questions so each quiz feels different every time.
from question_bank import questions_by_subject  # This imports a predefined question bank for each subject.

# Function to gather user details: name, age, and year level.
def get_user_details():
    # Prompts the user to enter their name in a simple text box.
    name = easygui.enterbox("Enter your name:", title="Quiz Login")
    
    # Prompts the user to enter their age, setting a valid range (0 to 120).
    age = easygui.integerbox("Enter your age:", title="Quiz Age Verification", lowerbound=0, upperbound=120)
    
    # If the user is under 10, the program will stop here, letting them know they're too young.
    if age <= 9:
        easygui.msgbox("Sorry, you are ineligible for the quiz due to age restrictions.", title="Ineligible")
        return None  # Stops the quiz if the user isn't eligible due to age.
    else:
        # If the user is eligible, they get a welcome message.
        easygui.msgbox(f"Welcome, {name}! You are eligible for the quiz.", title="Welcome")
    
    # Asks for their year level (though not necessary for the quiz itself, it's nice to personalize!).
    year_level = easygui.enterbox("Enter your year level:", title="Year Level")
    
    # Returns all the gathered details so the program can use them later.
    return name, age, year_level

# Function to let the user choose a subject for the quiz.
def select_subject():
    # List all subjects available from the question bank, using the keys from the imported dictionary.
    subjects = list(questions_by_subject.keys())
    
    # Asks the user to select a subject from the list in a simple choice dialog.
    subject = easygui.choicebox("Available subjects are:", title="Select Subject", choices=subjects)
    
    # Returns the selected subject, or None if the user cancels.
    return subject

# Function to display each question, choices, and check the user's answer.
def ask_question(question, choices, answer):
    # Formats the choices like 'a. option1', 'b. option2', etc., to make the selection clearer.
    choice_string = [f"{chr(97 + i)}. {choices[i]}" for i in range(len(choices))]  # Using chr(97) to start at 'a'.
    
    # Shows the question and choices in a buttonbox for the user to select from.
    user_response = easygui.buttonbox(question, title="Quiz Question", choices=choice_string)
    
    # Maps the correct answer's index to a formatted string like 'a. option1', for comparison later.
    correct_response = f"{answer}. {choices[ord(answer) - ord('a')]}"
    
    # Checks if the user's response matches the correct answer.
    if user_response == correct_response:
        # If correct, show a message saying "Correct!"
        easygui.msgbox("Correct!", title="Result")
        return True  # Return True to indicate the answer was correct.
    else:
        # If incorrect, show the correct answer to the user.
        easygui.msgbox(f"Incorrect. The correct answer was: {correct_response}", title="Result")
        return False  # Return False to indicate the answer was wrong.

# This function handles the quiz for a specific subject, asking each question and tracking the score.
def quiz_on_subject(subject):
    # Get all the questions for the selected subject.
    questions = questions_by_subject[subject]
    
    # Shuffle the questions so the quiz feels fresh each time.
    random.shuffle(questions)
    
    # Start with a score of 0.
    score = 0
    
    # Loop through each question, choices, and answer.
    for question, choices, answer in questions:
        # If the user answers correctly, increment their score by 1.
        if ask_question(question, choices, answer):
            score += 1
    
    # After all the questions are done, return the final score.
    return score

# Main function to run the quiz.
def main():
    # First, get the user's details. If they're ineligible (age below 10), the function will return None and stop here.
    user_info = get_user_details()
    if user_info is None:
        return  # If the user is ineligible, exit the quiz program.
    
    # Unpack the user's details (name, age, and year level) for future use.
    name, age, year_level = user_info

    # Start a loop to allow the user to take multiple quizzes if they choose.
    while True:
        # Ask the user to select a subject for their quiz.
        subject = select_subject()
        
        # If the user cancels the subject selection, break out of the loop and end the quiz.
        if not subject:
            break  # Exit if no subject is chosen.
        
        # Run the quiz for the selected subject, and get the score.
        score = quiz_on_subject(subject)
        
        # Show the user their score after completing the quiz.
        easygui.msgbox(f"You completed the {subject} quiz. Your current score is {score}.", title="Quiz Completed")
        
        # Ask if they want to take another quiz. If they say no, end the program.
        if not easygui.ynbox("Would you like to pick another subject?", title="Continue?", choices=["Yes", "No"]):
            # If the user chooses not to continue, show them a final message with their total score and exit.
            easygui.msgbox(f"Thank you, {name}! Your total score is {score}.", title="Goodbye")
            break  # End the quiz loop.

# Standard Python boilerplate to run the main function if this file is executed directly.
if __name__ == "__main__":
    main()
