
from flask import Flask, request
import joblib

pancakes = Flask(__name__)

# Load the trained machine learning model
clf = joblib.load('classifier.pkl')


# Home route
@pancakes.route('/', methods=['GET'])
def hello():
    return {"message": "Hello, World!"}


# Hello route
@pancakes.route('/hello', methods=['GET'])
def hello_name():
    name = request.args.get('name', 'World')
    return {"message": f"Hello, {name}!"}


# Loan prediction route
@pancakes.route('/predict', methods=['POST'])
def predict():

    loan_req = request.get_json()

    if not loan_req:
        return {"error": "Invalid JSON input"}, 400

    # Convert categorical values into numerical values

    if loan_req['Gender'] == "Male":
        Gender = 0
    else:
        Gender = 1

    if loan_req['Married'] == "Unmarried":
        Married = 0
    else:
        Married = 1

    if loan_req['Credit_History'] == "Uncleared Debts":
        Credit_History = 0
    else:
        Credit_History = 1

    # Extract numerical values
    ApplicantIncome = loan_req['ApplicantIncome']
    LoanAmount = loan_req['LoanAmount']

    # Make prediction
    prediction = clf.predict(
        [[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]]
    )[0]

    # Display prediction result
    if prediction == 0:
        result = "Loan Rejected"
    else:
        result = "Loan Approved"

    return {"loan_approval_status": result}

#curl --location 'http://127.0.0.1:5000/predict' \
#--header 'Content-Type: application/json' \
#--data '{
    "Gender": "Male",
    "Married": "Unmarried",
    "Credit_History": "Cleared Debts",
    "ApplicantIncome": 50000,
    "LoanAmount": 50000000
#}'