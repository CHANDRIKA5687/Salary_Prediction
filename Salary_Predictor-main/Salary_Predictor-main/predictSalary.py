import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from word2number import w2n
from sklearn import linear_model

# Load the dataset
df = pd.read_csv('expected_salary.csv')

# Fill missing values in 'experience' and 'test_score' columns
df['experience'] = df['experience'].fillna('zero')
df['test_score'] = df['test_score'].fillna(df['test_score'].median())

# Convert 'experience' values from words to numbers
df['experience'] = df['experience'].apply(w2n.word_to_num)

# Ensure 'experience' and 'test_score' are of integer type
df['experience'] = df['experience'].astype(int)
df['test_score'] = df['test_score'].astype(int)

# Fit a linear regression model
model = linear_model.LinearRegression()
input_data = df.drop(columns='salary')
output_data = df.salary
model.fit(input_data, output_data)

# Define a function to predict salary for eligible employees
def predict_salary(experience, test_score, interview_score):
    if experience == 0:
        if test_score == 0 or interview_score == 0:
            return "Not eligible employee"
        else:
            return model.predict([[experience, test_score, interview_score]])[0]
    elif test_score == 0:
        return "Improve your test skills and Try Again!!"
    elif interview_score == 0:
        return "Improve interview performance and Try Again!!"
    elif test_score < 5 and interview_score < 5:
        return "Predicted Salary: 24000.00"  # Set the salary to $24,000 if both scores are below 5
    elif test_score > 5 and interview_score < 5:
        return "Predicted Salary: 45000.00"  # Set the salary to $45,000 if test score is above 5 but interview score is less than 5
    else:
        salary_prediction = model.predict([[experience, test_score, interview_score]])[0]
        if test_score < 5 and interview_score >= 5:
            salary_prediction *= 1.1  # Increase salary if low test score but good interview score
        elif test_score >= 5 and interview_score < 5:
            salary_prediction *= 0.9  # Decrease salary if good test score but low interview score
        return f"Predicted Salary: {salary_prediction:.2f}"

# Function to predict and display salary
def predict_and_display_salary():
    experience = int(experience_entry.get())
    test_score = int(test_score_entry.get())
    interview_score = int(interview_score_entry.get())

    result = predict_salary(experience, test_score, interview_score)
    result_label.config(text=result)

# Create a Tkinter window
window = Tk()
window.title("Salary Prediction")
window.geometry("400x300")  # Increase the window size

# Change the background color to faint pink
window.configure(bg="#FFDDDD")

# Create input fields and labels without a background color
experience_label = Label(window, text="Experience:", fg="black", bg="#FFDDDD")
experience_label.pack(fill='x', padx=10, pady=5)
experience_entry = Entry(window)
experience_entry.pack(fill='x', padx=10, pady=5)
test_score_label = Label(window, text="Test Score:", fg="black", bg="#FFDDDD")
test_score_label.pack(fill='x', padx=10, pady=5)
test_score_entry = Entry(window)
test_score_entry.pack(fill='x', padx=10, pady=5)
interview_score_label = Label(window, text="Interview Score:", fg="black", bg="#FFDDDD")
interview_score_label.pack(fill='x', padx=10, pady=5)
interview_score_entry = Entry(window)
interview_score_entry.pack(fill='x', padx=10, pady=5)

# Create a button for prediction with blue color
predict_button = Button(window, text="Predict Salary", command=predict_and_display_salary, bg="blue", fg="white")
predict_button.pack(fill='x', padx=10, pady=10)

# Create a label for displaying the result
result_label = Label(window, text="Predicted Salary: ")
result_label.pack(fill='x', padx=10, pady=5)

window.mainloop()
