import pandas as pd
import matplotlib.pyplot as plt
import warnings
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

# Suppress the warning about feature names not being available
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Fit a linear regression model
model = linear_model.LinearRegression()
input_data = df.drop(columns='salary')
output_data = df.salary
model.fit(input_data, output_data)

# Define a function to predict salary for eligible employees
def predict_salary(experience, test_score, interview_score):
    if test_score == 0 and interview_score == 0:
        return "Not eligible"
    elif test_score == 0:
        return "Not eligible for interview"
    elif interview_score == 0:
        return "Improve your communication"
    elif experience == 0:
        return "No worries, we can predict salary as a fresher based on interview and test score"
    else:
        salary_prediction = model.predict([[experience, test_score, interview_score]])[0]
        if test_score < 5 and interview_score >= 5:
            salary_prediction *= 1.1  # Increase salary if low test score but good interview score
        elif test_score >= 5 and interview_score < 5:
            salary_prediction *= 0.9  # Decrease salary if good test score but low interview score
        return salary_prediction

# Example usage of the predict_salary function
predicted_salary = predict_salary(0, 0, 0)

# Print the appropriate message
print(predicted_salary)
