import requests
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
API_KEY = "bkX9c9YmJOMU5-xLWG5byUeIpQ_iQKu5eqBbq9Ib_7lK"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__,template_folder="Template")
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/home1')
def home1():
    return render_template("index.html")
@app.route("/assesment")
def home():
    return render_template('Demo2.html')
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/y_predict", methods = ['POST'])
def y_predict():
    min1 = [290.0, 92.0, 1.0, 1.0, 1.0, 6.8, 0.0]
    max1 = [340.0, 120.0, 5.0, 5.0, 5.0, 9.92, 1.0]
    gre = float(request.form['t1'])
    toefl = float(request.form['t2'])
    rating = float(request.form['University'])
    sop = float(request.form['sop'])
    lor = float(request.form['lor'])
    cgpa = float(request.form['cgpa'])
    research = float(request.form['research'])

    X = [[t1,t2,University,sop,lor,cgpa,research]]
    payload_scoring = {"input_data": [{"field": [['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR ','CGPA','Research']],"values": X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/28992166-bd24-44d9-9304-7a6d70867b64/predictions?version=2022-10-18', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)

    pred = response_scoring.json()

    output = pred['predictions'][0]['values'][0][0]

    if(output==False):
        return render_template('noChance.html', prediction_text='You Dont have a chance of getting admission')
    else:
        return render_template('chance.html', prediction_text='You have a chance of getting admission')
if __name__ == "__main__":
    app.run(debug=False)

