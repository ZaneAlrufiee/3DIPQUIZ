import random  # Importing the random module to help us shuffle our quiz questions.

# This dictionary holds all our quiz questions, organized by subject.
# Each subject has a list of tuples, where each tuple contains a question,
# the possible answers, and the key to the correct answer.
questions_by_subject = {
    "Politics": [
        ("Who is the current President of the United States?",  # A question about U.S. politics
         ["a. Barack Obama", "b. Donald Trump", "c. Joe Biden", "d. George Bush"],  # Possible answers
         "c"),  # The correct answer
        ("What is the capital of Japan?", 
         ["a. Shanghai", "b. Beijing", "c. Tokyo", "d. Seoul"], 
         "c")
    ],
    "Art": [
        ("Who painted the Mona Lisa?",  # A question about art history
         ["a. Michelangelo", "b. Leonardo da Vinci", "c. Vincent van Gogh", "d. Pablo Picasso"], 
         "b"),
        ("What is the highest mountain in Africa?", 
         ["a. Mount Everest", "b. Mount Kilimanjaro", "c. Mount Fuji", "d. Mount McKinley"], 
         "b")
    ],
    # You can add more subjects and questions here to make the quiz even more fun!
}

def select_subject():
    """
    This function lets the user pick a subject for their quiz.
    It keeps asking until the user provides a valid subject.
    """
    subjects = list(questions_by_subject.keys())  # Grab the available subjects from our dictionary.
    while True:
        print("Available subjects are:", ', '.join(subjects))  # Show the user the subjects they can choose from.
        subject = input("Enter the subject you want to be quizzed on: ").capitalize()  # Get the user's choice and make it pretty.
        # Check if the subject they picked is valid.
        if subject in subjects:
            return subject  # Return the chosen subject.
        else:
            print("Hmm, that doesn't seem like a valid subject. Try again!")  # Let them know they messed up.

def ask_question(question, choices, answer):
    """
    This function displays a question and its choices to the user.
    It checks their answer and gives feedback.
    """
    print(question)  # Show the question.
    for choice in choices:  # Loop through the answer choices and display them.
        print(choice)  # Print each choice for the user.
    
    # Ask the user for their answer, giving them options to skip or reset the quiz.
    response = input("Please enter your response (or type 'skip' to skip, 'reset' to start over): ").lower()
    
    # Check the user's answer and give them feedback.
    if response == answer:
        print("That's correct! Well done!")  # If they got it right, cheer them on.
        return True  # Indicate a correct answer.
    elif response == "skip":
        print("You've skipped this question.")  # Let them know they chose to skip.
        return False  # Return False for the skipped question.
    elif response == "reset":
        return "reset"  # Let us know they want to start over.
    else:
        print("Oops, that's not correct.")  # If they got it wrong, let them know.
        print("The right answer was:", answer)  # Show them the correct answer.
        return False  # Return False for an incorrect answer.

def quiz_on_subject(subject):
    """
    This function runs the quiz for the selected subject.
    It shuffles the questions and keeps track of how many the user got right.
    """
    questions = questions_by_subject[subject]  # Get the questions for the chosen subject.
    random.shuffle(questions)  # Shuffle the questions to make things interesting.
    
    correct = 0  # Counter for correct answers.
    incorrect = 0  # Counter for incorrect answers.
    
    # Go through each question and see how the user does.
    for question, choices, answer in questions:
        result = ask_question(question, choices, answer)  # Ask the question and get their answer.
        
        if result == "reset":
            return "reset"  # If they want to reset, let us know.
        elif result:
            correct += 1  # They got it right, so increase the correct count.
        else:
            incorrect += 1  # They got it wrong, so increase the incorrect count.
    
    # Once all questions are done, show the user their results.
    print(f"\nYou've finished the {subject} quiz! You got {correct} right and {incorrect} wrong.")

def main():
    """
    The main function to run our quiz program.
    This is where everything comes together.
    """
    while True:
        # Start the quiz process: select a subject and take the quiz.
        subject = select_subject()  # Ask the user to pick a subject.
        result = quiz_on_subject(subject)  # Run the quiz for that subject.
        
        if result == "reset":
            continue  # If they reset, just start the quiz over.
        
        # Ask the user if they want to keep playing or exit.
        if input("Type 'yes' if you want to pick another subject, or any other key to exit: ").lower() != "yes":
            break  # If they don’t want to continue, end the loop and exit.

# This block checks if the script is being run directly (not imported).
if __name__ == "__main__":
    main()  # Start the quiz program when the script is run directly.
