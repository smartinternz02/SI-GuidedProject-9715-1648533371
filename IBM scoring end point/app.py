from unicodedata import category
from flask import Flask, render_template, request
import requests
import pickle

app = Flask(__name__)
sc = pickle.load(open('transform.pkl', 'rb'))

API_KEY = "MlEgdJkf522GrTbatQCJhmp7vteXE4EGPhtuDyR1bb81"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        cc = float(request.form.get('cloudCover'))
        ar = float(request.form.get('aRain'))
        jfr = float(request.form.get('jfRain'))
        mmr = float(request.form.get('mmRain'))
        jsr = float(request.form.get('jsRain'))
        arr = [[cc, ar, jfr, mmr, jsr]]
        payload_scoring = {"input_data": [{"fields": [["cc", "ar", "jfr", "mmr", "jsr"]], "values": arr}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1b72232a-1738-4268-8216-6d90313e72bc/predictions?version=2022-06-02', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})

        pred = response_scoring.json()
        val = pred["predictions"][0]['values'][0][0]
        print(val)
        if(round(val)==1):
            final = "Possibility of severe flood"
        else:
            final = "No possibility of severe flood"
    else:
        final = ""
    return render_template("predict.html", y=final)

if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = 'qwerty123'