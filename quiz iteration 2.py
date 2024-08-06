import random

# This dictionary organizes quiz questions by subject. Each entry contains a subject as the key and a list of tuples for the questions. 
# Each tuple includes the question text, a list of multiple-choice options, and the correct answer's letter as a string.
questions_by_subject = {
    "Politics": [
        ("Who is the current President of the United States?", ["a. Barack Obama", "b. Donald Trump", "c. Joe Biden", "d. George Bush"], "c"),
        ("What is the capital of Japan?", ["a. Shanghai", "b. Beijing", "c. Tokyo", "d. Seoul"], "c")
    ],
    "Art": [
        ("Who painted the Mona Lisa?", ["a. Michelangelo", "b. Leonardo da Vinci", "c. Vincent van Gogh", "d. Pablo Picasso"], "b"),
        ("What is the highest mountain in Africa?", ["a. Mount Everest", "b. Mount Kilimanjaro", "c. Mount Fuji", "d. Mount McKinley"], "b")
    ],
    # More subjects are defined in a similar manner...
}

def select_subject():
    # Convert the dictionary keys into a list for easier access and display them to the user.
    subjects = list(questions_by_subject.keys())
    while True:
        print("Available subjects are:", ', '.join(subjects))
        # Ask the user to input their choice of subject.
        subject = input("Enter the subject you want to be quizzed on: ").capitalize()
        # Check if the input matches any subject in the list.
        if subject in subjects:
            return subject  # Return the valid subject.
        else:
            print("Invalid subject, please try again.")  # Prompt again if the input is invalid.

def ask_question(question, choices, answer):
    # Display the question and choices.
    print(question)
    for choice in choices:
        print(choice)
    # Get the user's answer, allowing for commands to skip or reset.
    response = input("Please enter your response (or enter 'skip' to skip, 'reset' to reset the quiz): ").lower()
    # Evaluate the response and provide appropriate feedback.
    if response == answer:
        print("Correct!")
        return True
    elif response == "skip":
        print("Question skipped.")
        return False
    elif response == "reset":
        return "reset"  # Return a special flag to reset the quiz.
    else:
        print("Incorrect.")
        print("The correct answer was:", answer)
        return False

def quiz_on_subject(subject):
    # Retrieve the questions for the chosen subject and shuffle them.
    questions = questions_by_subject[subject]
    random.shuffle(questions)
    correct = 0
    incorrect = 0
    # Loop through each question and process the answers.
    for question, choices, answer in questions:
        result = ask_question(question, choices, answer)
        if result == "reset":
            return "reset"  # Handle the reset command.
        elif result:
            correct += 1  # Increment the count of correct answers.
        else:
            incorrect += 1  # Increment the count of incorrect or skipped answers.
    # Once all questions are asked, print the results.
    print(f"\nFinished {subject} quiz. You answered {correct} questions correctly and {incorrect} questions incorrectly.")

def main():
    while True:
        # Run the quiz process: select a subject and take the quiz.
        subject = select_subject()
        result = quiz_on_subject(subject)
        if result == "reset":
            continue  # Restart the quiz if 'reset' was triggered.
        # Ask if the user wants to continue with another quiz.
        if input("Enter 'yes' to pick another subject or any other key to exit: ").lower() != "yes":
            break  # Exit the loop and end the program if the user does not type 'yes'.

if __name__ == "__main__":
    main()  # Ensures that the main function is called only if the script is run directly.
