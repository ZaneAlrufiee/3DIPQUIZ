import random  # We're importing the random module to help shuffle our quiz questions.
from question_bank import questions_by_subject  # Importing our question bank containing subjects and questions.

# Let's get the user details up front.
name = input("Enter your name: ")  # Ask for the user's name.
age = int(input("Enter your age: "))  # Get the user's age and convert it to an integer.
year_level = input("Enter your year level: ")  # Ask for the user's year level.

# Check if the user is old enough for the quiz.
if age <= 9:
    print("Sorry, you are ineligible for the quiz due to age restrictions.")  # Inform the user if they're too young.
    exit()  # End the program if they're ineligible.
else:
    print(f"Welcome, {name}! You are eligible for the quiz.")  # Welcome the user if they meet age criteria.

score = 0  # Initialize the user's score to 0.

def select_subject():
    """
    This function lets the user choose a subject for their quiz.
    It keeps asking until the user provides a valid subject.
    """
    subjects = list(questions_by_subject.keys())  # Get the available subjects from our question bank.
    print("Available subjects are:", ', '.join(subjects))  # Show the subjects the user can choose from.
    
    while True:
        subject = input("Enter the subject you want to be quizzed on: ").capitalize()  # Ask for the user's choice and format it.
        if subject in subjects:
            return subject  # Return the chosen subject if it's valid.
        else:
            print("Invalid subject, please try again.")  # If invalid, prompt the user to try again.

def ask_question(question, choices, answer):
    """
    This function presents a question to the user, checks their answer, and updates the score.
    """
    print(question)  # Display the question to the user.
    for choice in choices:  # Loop through the answer choices and show them.
        print(choice)  # Print each choice for the user to see.
    
    response = input("Enter your response (a, b, c, or d): ").lower()  # Get the user's answer.
    
    if response == answer:  # Check if the user's response is correct.
        print("Correct!")  # Let them know they got it right.
        global score  # Access the global score variable.
        score += 1  # Increment the score by 1 for a correct answer.
    else:
        print("Incorrect. The correct answer was:", answer)  # Inform them if they got it wrong.

def quiz_on_subject(subject):
    """
    This function runs the quiz for the selected subject,
    shuffling the questions and asking each one in turn.
    """
    questions = questions_by_subject[subject]  # Get the questions for the chosen subject.
    random.shuffle(questions)  # Shuffle the questions for variety.
    
    for question, choices, answer in questions:  # Loop through each question in the shuffled list.
        ask_question(question, choices, answer)  # Ask the question and check the user's answer.

def main():
    """
    This is the main function that keeps the quiz program running.
    It allows the user to select subjects and take quizzes until they choose to exit.
    """
    while True:
        subject = select_subject()  # Ask the user to pick a subject for their quiz.
        quiz_on_subject(subject)  # Run the quiz for that subject.
        print(f"Finished {subject} quiz. Your current score is {score}.")  # Show the user their score after finishing.
        
        # Ask if they want to try another subject or exit the program.
        if input("Enter 'yes' to pick another subject or any other key to exit: ").lower() != "yes":
            print(f"Thank you, {name}! Your total score is {score}.")  # Thank the user and show their total score.
            break  # Exit the loop and end the program.

# This block checks if the script is being run directly (not imported).
if __name__ == "__main__":
    main()  # Start the quiz program when the script is executed directly.
