from unicodedata import category
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('transform.pkl', 'rb'))

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
        val = model.predict(sc.transform(arr))
        if(round(val[0])==1):
            final = "Possibility of severe flood"
        else:
            final = "No possibility of severe flood"
    else:
        final = ""
    return render_template("predict.html", y=final)

if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = 'qwerty123'