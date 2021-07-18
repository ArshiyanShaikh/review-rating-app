from flask import request,render_template,Flask
from flask.signals import request_tearing_down
import numpy as np
from nltk.corpus import stopwords
import re
import pickle
stopwrds = stopwords.words('english')


model_fpath ='./statics/rating_model.sav'
clf = pickle.load(open(model_fpath, 'rb'))
vect_path = './statics/vectorizer.sav'
vect = pickle.load(open(vect_path, 'rb'))




def preprocess_text(text:str) -> str:
    text = text.lower()
    text = [t for t in re.findall('\w+',text) if t not in stopwrds ]
    text = [t for t in text if len(t) > 1]
    return " ".join(text)


user_name = 'admin'
passowrd = 'admin123'

app = Flask(__name__)  # initialize Flask 


@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        print(login)
        if (login == 'admin') & (password =='admin123'):
            return render_template('index.html')
        else:
            return "<h1>Credntial Failed</h1>"
    return render_template('login.html')

@app.route("/product_review",methods =['GET','POST'])

def rating_prediction():
    if request.method == 'POST':
        review = request.form.get('review')
        
        vector = vect.transform([review])
        rating= clf.predict(vector)
        return render_template('index.html',rating =rating[0],review =review)
    return render_template("index.html")



if __name__=='__main__':
    app.run(debug=True)