import random

# Dictionary to store quiz questions organized by subject.
# Each subject has a list of tuples containing the question text, possible answers, and the correct answer key.
questions_by_subject = {
    "Politics": [
        ("Who is the current President of the United States?", ["a. Barack Obama", "b. Donald Trump", "c. Joe Biden", "d. George Bush"], "c"),
        ("What is the capital of Japan?", ["a. Shanghai", "b. Beijing", "c. Tokyo", "d. Seoul"], "c")
    ],
    "Art": [
        ("Who painted the Mona Lisa?", ["a. Michelangelo", "b. Leonardo da Vinci", "c. Vincent van Gogh", "d. Pablo Picasso"], "b"),
        ("What is the highest mountain in Africa?", ["a. Mount Everest", "b. Mount Kilimanjaro", "c. Mount Fuji", "d. Mount McKinley"], "b")
    ],
    # More subjects and their questions added here...
}

def select_subject():
    # List all available subjects by retrieving keys from the dictionary.
    subjects = list(questions_by_subject.keys())
    while True:
        print("Available subjects are:", ', '.join(subjects))
        subject = input("Enter the subject you want to be quizzed on: ").capitalize()
        # Validate the user's input. If it's a valid subject, return it.
        if subject in subjects:
            return subject
        else:
            print("Invalid subject, please try again.")

def ask_question(question, choices, answer):
    print(question)
    # Display all answer choices for the current question.
    for choice in choices:
        print(choice)
    # Prompt the user for a response. They can also choose to skip or reset.
    response = input("Please enter your response (or enter 'skip' to skip, 'reset' to reset the quiz): ").lower()
    # Check the user's response and provide appropriate feedback.
    if response == answer:
        print("Correct!")
        return True
    elif response == "skip":
        print("Question skipped.")
        return False
    elif response == "reset":
        return "reset"
    else:
        print("Incorrect.")
        print("The correct answer was:", answer)
        return False

def quiz_on_subject(subject):
    # Retrieve questions for the chosen subject and shuffle them to randomize the order.
    questions = questions_by_subject[subject]
    random.shuffle(questions)
    correct = 0
    incorrect = 0
    # Loop through each question and process the user's answer.
    for question, choices, answer in questions:
        result = ask_question(question, choices, answer)
        if result == "reset":
            return "reset"  # Allows the user to restart the quiz.
        elif result:
            correct += 1  # Increment correct answer count.
        else:
            incorrect += 1  # Increment incorrect answer count.
    # After all questions are answered, print the quiz results.
    print(f"\nFinished {subject} quiz. You answered {correct} questions correctly and {incorrect} questions incorrectly.")

def main():
    while True:
        # Run the quiz process: select a subject, take the quiz.
        subject = select_subject()
        result = quiz_on_subject(subject)
        if result == "reset":
            continue  # If 'reset' was triggered, restart the quiz without exiting.
        # Ask the user if they want to continue with another subject or exit.
        if input("Enter 'yes' to pick another subject or any other key to exit: ").lower() != "yes":
            break  # Exit the loop (and the program) if the user doesn't type 'yes'.

if __name__ == "__main__":
    main()  # Only run the main function when the script is executed directly (not imported).
