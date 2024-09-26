import easygui
import random
from question_bank import questions_by_subject  # Importing our questions categorized by subject

class QuizApp:
    def __init__(self):
        # Initializing user details and total score
        self.name = None  # Placeholder for the user's name
        self.age = None   # Placeholder for the user's age
        self.year_level = None  # Placeholder for the user's year level
        self.total_score = 0  # Starting score is zero

    def get_user_details(self):
        # Collecting user details to ensure eligibility for the quiz
        self.name = easygui.enterbox("Enter your name:", title="Quiz Login")
        if not self.name:  # Check if the name was entered
            easygui.msgbox("Name is required to start the quiz.", title="Error")
            return False  # Return False if name is not provided
        
        # Ask for the user's age and verify eligibility
        self.age = easygui.integerbox("Enter your age:", title="Quiz Age Verification", lowerbound=5, upperbound=120)
        if self.age is None or self.age <= 9:  # Check if age is below 10
            easygui.msgbox("Sorry, you are ineligible for the quiz due to age restrictions.", title="Ineligible")
            return False  # Return False if ineligible
        
        easygui.msgbox(f"Welcome, {self.name}! You are eligible for the quiz.", title="Welcome")
        self.year_level = easygui.enterbox("Enter your year level:", title="Year Level")  # Get the year level of the user
        return True  # Return True if all details are collected successfully

    def select_subject(self):
        # Allowing the user to select a subject for the quiz
        subjects = list(questions_by_subject.keys())  # Get the list of available subjects
        if not subjects:  # Check if there are no subjects
            easygui.msgbox("No subjects available at the moment.", title="No Subjects")
            return None  # Return None if no subjects are found
        
        # Show a selection box for the user to choose a subject
        subject = easygui.choicebox("Select a subject:", title="Quiz Subjects", choices=subjects)
        return subject  # Return the chosen subject

    def ask_question(self, question, choices, answer):
        # Asking the user a question and checking their response
        choice_labels = [f"{chr(97 + i)}. {choices[i]}" for i in range(len(choices))]  # Create labels like 'a. choice1'
        user_response = easygui.buttonbox(question, title="Quiz Question", choices=choice_labels)  # Display the question
        
        # Determine the correct choice based on the answer
        correct_choice = choice_labels[ord(answer) - ord('a')]  # Convert answer letter to choice label
        if user_response == correct_choice:  # Check if the user's response matches the correct answer
            easygui.msgbox("Correct!", title="Result")  # Notify the user they were correct
            return True  # Return True for a correct answer
        else:
            easygui.msgbox(f"Incorrect. The correct answer was: {correct_choice}", title="Result")  # Inform them of the correct answer
            return False  # Return False for an incorrect answer

    def quiz_on_subject(self, subject):
        # Conduct the quiz for the selected subject
        questions = questions_by_subject.get(subject, [])  # Get questions for the chosen subject
        if not questions:  # Check if there are no questions available
            easygui.msgbox(f"No questions available for {subject}.", title="No Questions")
            return 0  # Return 0 if no questions to ask

        random.shuffle(questions)  # Shuffle questions to make the quiz different each time
        score = 0  # Initialize score for this subject quiz
        for question, choices, answer in questions:  # Loop through each question
            if self.ask_question(question, choices, answer):  # Ask the question and check the response
                score += 1  # Increase score for each correct answer
        
        # Notify the user of their score for the completed quiz
        easygui.msgbox(f"You completed the {subject} quiz with a score of {score}/{len(questions)}.", title="Quiz Completed")
        return score  # Return the score achieved

    def run(self):
        # Main function to run the quiz application
        if not self.get_user_details():  # Get user details; exit if ineligible
            return
        
        while True:  # Loop to allow multiple quizzes
            subject = self.select_subject()  # Ask user to select a subject
            if not subject:  # Check if user cancels the selection
                easygui.msgbox(f"Thank you for participating, {self.name}! Your final score is {self.total_score}.", title="Goodbye")
                break  # Exit the loop and end the quiz
            
            self.total_score += self.quiz_on_subject(subject)  # Add the score from the quiz to the total score
            
            # Ask if the user wants to take another quiz
            if not easygui.ynbox("Would you like to take another quiz?", title="Continue?", choices=["Yes", "No"]):
                easygui.msgbox(f"Thank you for participating, {self.name}! Your final score is {self.total_score}.", title="Goodbye")
                break  # Exit the loop if the user does not want to continue

if __name__ == "__main__":
    quiz_app = QuizApp()  # Create an instance of the QuizApp class
    quiz_app.run()  # Run the quiz application
