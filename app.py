
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request,Flask
from werkzeug.security import generate_password_hash,check_password_hash
from flask_pymongo import PyMongo
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import pickle

corpus = []
app= Flask(__name__)
app.secret_key="secretkey"
app.config['MONGO_URI']="mongodb://localhost:27017/shopDatabase"
mongo=PyMongo(app)




@app.route("/users")
def findusers():
    users=mongo.db.users.find()
    resp=dumps(users)
    print(resp)
    return(resp)

@app.route("/user/<Password>")  
def finduser(Password):
    print(Password)
    user=mongo.db.users.find_one({"password":Password})  
    resp=dumps(user)
    print(resp)
    return(resp)
@app.route("/user/insert",methods=["POST"])
def putuser():
    res=request.form["newone"]
    print(res)
    

    # id=mongo.db.users.insert_one({"name":_name,
    # "email":"souvi@gmail.com",
    # "password":"98740",
    # "address1":"ajsdhkjadh"
    # })
    # print("insert")
    return(res)

@app.route("/souvikNLP",methods=["POST"])
    
def filter():
    cv = pickle.load(open('vectorizer.pickle', 'rb'))
    classifier_f=open("naivebayes.pickle","rb")
    classifier=pickle.load(classifier_f)
    classifier_f.close()
    new_review=request.form["comment"]
    new_review = re.sub('[^a-zA-Z]', ' ', new_review)
    new_review = new_review.lower()
    new_review = new_review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
    new_review = ' '.join(new_review)
    new_corpus = [new_review]

    new_X_test = cv.transform(new_corpus).toarray()
    new_y_pred = classifier.predict(new_X_test)
    return jsonify({'predictions' : new_y_pred.tolist()})
    


if __name__=="__main__":
    app.run()
