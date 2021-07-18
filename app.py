from flask import request,render_template,Flask
from flask.signals import request_tearing_down
import numpy as np
import re
import pickle

stopwrds = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


model_fpath ='./static/rating_model.sav'
clf = pickle.load(open(model_fpath, 'rb'))
vect_path = './static/vectorizer.sav'
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
    return render_template("login.html")



if __name__=='__main__':
    app.run(debug=True)
