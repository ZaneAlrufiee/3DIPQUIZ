import random

# Define the questions as a dictionary, where keys are subjects and values are lists of tuples with questions, choices, and correct answers.
questions_by_subject = {
    "Politics": [
        ("Who is the current President of the United States?", ["a. Barack Obama", "b. Donald Trump", "c. Joe Biden", "d. George Bush"], "c"),
        ("What is the capital of Japan?", ["a. Shanghai", "b. Beijing", "c. Tokyo", "d. Seoul"], "c")
    ],
    "Art": [
        ("Who painted the Mona Lisa?", ["a. Michelangelo", "b. Leonardo da Vinci", "c. Vincent van Gogh", "d. Pablo Picasso"], "b"),
        ("What is the highest mountain in Africa?", ["a. Mount Everest", "b. Mount Kilimanjaro", "c. Mount Fuji", "d. Mount McKinley"], "b")
    ],
    "Science": [
        ("What is the largest planet in our solar system?", ["a. Mars", "b. Venus", "c. Jupiter", "d. Saturn"], "c"),
        ("What is the chemical symbol for gold?", ["a. Ag", "b. Au", "c. Cu", "d. Fe"], "b")
    ],
    "Geography": [
        ("What is the smallest country in the world?", ["a. Monaco", "b. Vatican City", "c. Liechtenstein", "d. San Marino"], "b"),
        ("Which of the following is not a primary color?", ["a. Red", "b. Blue", "c. Green", "d. Yellow"], "c")
    ],
    "Literature": [
        ("Who wrote the novel 'To Kill a Mockingbird'?", ["a. Harper Lee", "b. Ernest Hemingway", "c. William Faulkner", "d. F. Scott Fitzgerald"], "a")
    ]
}

def select_subject():
    subjects = list(questions_by_subject.keys())
    while True:
        print("Available subjects are:", ', '.join(subjects))
        subject = input("Enter the subject you want to be quizzed on: ").capitalize()
        if subject in subjects:
            return subject
        else:
            print("Invalid subject, please try again.")

def ask_question(question, choices, answer):
    print(question)
    for choice in choices:
        print(choice)
    response = input("Please enter your response (or enter 'skip' to skip, 'reset' to reset the quiz): ").lower()
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
    questions = questions_by_subject[subject]
    random.shuffle(questions)
    correct = 0
    incorrect = 0
    for question, choices, answer in questions:
        result = ask_question(question, choices, answer)
        if result == "reset":
            return "reset"
        elif result:
            correct += 1
        else:
            incorrect += 1

    print(f"\nFinished {subject} quiz. You answered {correct} questions correctly and {incorrect} questions incorrectly.")

def main():
    while True:
        subject = select_subject()
        result = quiz_on_subject(subject)
        if result == "reset":
            continue
        if input("Enter 'yes' to pick another subject or any other key to exit: ").lower() != "yes":
            break

if __name__ == "__main__":
    main()
