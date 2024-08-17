import easygui
import random
import time
from question_bank import questions_by_subject

leaderboard = []  # Stores top 5 scores with user details

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

def ask_question(question, choices, answer, time_limit=10):
    choice_string = [f"{chr(97 + i)}. {choices[i]}" for i in range(len(choices))]  # Display choices as 'a. option'
    choice_string.append("Exit Quiz")  # Add an option to exit the quiz
    
    start_time = time.time()
    remaining_time = time_limit

    while remaining_time > 0:
        user_response = easygui.buttonbox(f"{question}\n\nTime remaining: {remaining_time} seconds", 
                                          title="Quiz Question", 
                                          choices=choice_string)
        if user_response is None or user_response == "Exit Quiz":
            return "exit"  # Handle the case where the user closes the dialog or chooses to exit
        
        if user_response:
            break

        remaining_time = time_limit - int(time.time() - start_time)

    if remaining_time <= 0:
        easygui.msgbox("Time's up! Moving to the next question.", title="Time Limit Exceeded")
        return False

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
        result = ask_question(question, choices, answer)
        if result == "exit":
            return score, True  # Exit the quiz
        elif result:
            score += 1
    return score, False  # Continue quiz

def update_leaderboard(name, score):
    leaderboard.append((score, name))
    leaderboard.sort(reverse=True, key=lambda x: x[0])
    leaderboard[:] = leaderboard[:5]  # Keep only top 5 scores

def show_leaderboard():
    if not leaderboard:
        easygui.msgbox("No scores recorded yet.", title="Leaderboard")
    else:
        leaderboard_text = "\n".join([f"{i+1}. {name} - {score}" for i, (score, name) in enumerate(leaderboard)])
        easygui.msgbox(f"Top 5 Scores:\n\n{leaderboard_text}", title="Leaderboard")

def main():
    user_info = get_user_details()
    if user_info is None:
        return  # Exit if the user is ineligible or closes the dialog

    name, age, year_level = user_info

    total_score = 0
    while True:
        subject = select_subject()
        if not subject:
            break  # User cancelled subject selection

        score, exited = quiz_on_subject(subject)
        total_score += score
        easygui.msgbox(f"You completed the {subject} quiz. Your current score for {subject} is {score}.", title="Quiz Completed")
        update_leaderboard(name, total_score)
        show_leaderboard()
        
        if exited or not easygui.ynbox("Would you like to pick another subject?", title="Continue?", choices=["Yes", "No"]):
            easygui.msgbox(f"Thank you, {name}! Your total score is {total_score}.", title="Goodbye")
            break

if __name__ == "__main__":
    main()
