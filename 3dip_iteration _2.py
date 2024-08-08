import random
from question_bank import questions_by_subject

# Define variables at the top of the program
name = input("Enter your name: ")
age = int(input("Enter your age: "))
year_level = input("Enter your year level : ")

# Check eligibility based on age
if age <= 9:
    print("Sorry, you are ineligible for the quiz due to age restrictions.")
    exit()
else:
    print(f"Welcome, {name}! You are eligible for the quiz.")

score = 0  # Initialize score

def select_subject():
    subjects = list(questions_by_subject.keys())
    print("Available subjects are:", ', '.join(subjects))
    while True:
        subject = input("Enter the subject you want to be quizzed on: ").capitalize()
        if subject in subjects:
            return subject
        else:
            print("Invalid subject, please try again.")

def ask_question(question, choices, answer):
    print(question)
    for choice in choices:
        print(choice)
    response = input("Enter your response (a, b, c, or d): ").lower()
    if response == answer:
        print("Correct!")
        global score
        score += 1
    else:
        print("Incorrect. The correct answer was:", answer)

def quiz_on_subject(subject):
    questions = questions_by_subject[subject]
    random.shuffle(questions)
    for question, choices, answer in questions:
        ask_question(question, choices, answer)

def main():
    while True:
        subject = select_subject()
        quiz_on_subject(subject)
        print(f"Finished {subject} quiz. Your current score is {score}.")
        if input("Enter 'yes' to pick another subject or any other key to exit: ").lower() != "yes":
            print(f"Thank you, {name}! Your total score is {score}.")
            break

if __name__ == "__main__":
    main()
