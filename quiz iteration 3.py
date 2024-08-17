import easygui
import random
from question_bank import questions_by_subject

def get_user_details():
    name = easygui.enterbox("Enter your name:", title="Quiz Login")
    age = easygui.integerbox("Enter your age:", title="Quiz Age Verification", lowerbound=0, upperbound=120)
    if age <= 9:
        easygui.msgbox("Sorry, you are ineligible for the quiz due to age restrictions.", title="Ineligible")
        return None
    else:
        easygui.msgbox(f"Welcome, {name}! You are eligible for the quiz.", title="Welcome")
    year_level = easygui.enterbox("Enter your year level:", title="Year Level")
    return name, age, year_level

def select_subject():
    subjects = list(questions_by_subject.keys())
    subject = easygui.choicebox("Available subjects are:", title="Select Subject", choices=subjects)
    return subject

def ask_question(question, choices, answer):
    choice_string = [f"{chr(97 + i)}. {choices[i]}" for i in range(len(choices))]  # Display choices as 'a. option'
    user_response = easygui.buttonbox(question, title="Quiz Question", choices=choice_string)
    correct_response = f"{answer}. {choices[ord(answer) - ord('a')]}"
    if user_response == correct_response:
        easygui.msgbox("Correct!", title="Result")
        return True
    else:
        easygui.msgbox(f"Incorrect. The correct answer was: {correct_response}", title="Result")
        return False

def quiz_on_subject(subject):
    questions = questions_by_subject[subject]
    random.shuffle(questions)
    score = 0
    for question, choices, answer in questions:
        if ask_question(question, choices, answer):
            score += 1
    return score

def main():
    user_info = get_user_details()
    if user_info is None:
        return  # Exit if the user is ineligible
    name, age, year_level = user_info

    while True:
        subject = select_subject()
        if not subject:
            break  # User cancelled subject selection
        score = quiz_on_subject(subject)
        easygui.msgbox(f"You completed the {subject} quiz. Your current score is {score}.", title="Quiz Completed")
        
        if not easygui.ynbox("Would you like to pick another subject?", title="Continue?", choices=["Yes", "No"]):
            easygui.msgbox(f"Thank you, {name}! Your total score is {score}.", title="Goodbye")
            break

if __name__ == "__main__":
    main()
