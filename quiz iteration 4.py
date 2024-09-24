import easygui
import random
from question_bank import questions_by_subject

class QuizApp:
    def __init__(self):
        self.name = None
        self.age = None
        self.year_level = None
        self.total_score = 0

    def get_user_details(self):
        self.name = easygui.enterbox("Enter your name:", title="Quiz Login")
        if not self.name:
            easygui.msgbox("Name is required to start the quiz.", title="Error")
            return False
        
        self.age = easygui.integerbox("Enter your age:", title="Quiz Age Verification", lowerbound=5, upperbound=120)
        if self.age is None or self.age <= 9:
            easygui.msgbox("Sorry, you are ineligible for the quiz due to age restrictions.", title="Ineligible")
            return False
        
        easygui.msgbox(f"Welcome, {self.name}! You are eligible for the quiz.", title="Welcome")
        self.year_level = easygui.enterbox("Enter your year level:", title="Year Level")
        return True

    def select_subject(self):
        subjects = list(questions_by_subject.keys())
        if not subjects:
            easygui.msgbox("No subjects available at the moment.", title="No Subjects")
            return None
        
        subject = easygui.choicebox("Select a subject:", title="Quiz Subjects", choices=subjects)
        return subject

    def ask_question(self, question, choices, answer):
        choice_labels = [f"{chr(97 + i)}. {choices[i]}" for i in range(len(choices))]
        user_response = easygui.buttonbox(question, title="Quiz Question", choices=choice_labels)
        
        correct_choice = choice_labels[ord(answer) - ord('a')]
        if user_response == correct_choice:
            easygui.msgbox("Correct!", title="Result")
            return True
        else:
            easygui.msgbox(f"Incorrect. The correct answer was: {correct_choice}", title="Result")
            return False

    def quiz_on_subject(self, subject):
        questions = questions_by_subject.get(subject, [])
        if not questions:
            easygui.msgbox(f"No questions available for {subject}.", title="No Questions")
            return 0

        random.shuffle(questions)
        score = 0
        for question, choices, answer in questions:
            if self.ask_question(question, choices, answer):
                score += 1
        
        easygui.msgbox(f"You completed the {subject} quiz with a score of {score}/{len(questions)}.", title="Quiz Completed")
        return score

    def run(self):
        if not self.get_user_details():
            return  # Exit if the user is ineligible or cancels the input
        
        while True:
            subject = self.select_subject()
            if not subject:
                easygui.msgbox(f"Thank you for participating, {self.name}! Your final score is {self.total_score}.", title="Goodbye")
                break
            
            self.total_score += self.quiz_on_subject(subject)
            
            if not easygui.ynbox("Would you like to take another quiz?", title="Continue?", choices=["Yes", "No"]):
                easygui.msgbox(f"Thank you for participating, {self.name}! Your final score is {self.total_score}.", title="Goodbye")
                break

if __name__ == "__main__":
    quiz_app = QuizApp()
    quiz_app.run()
