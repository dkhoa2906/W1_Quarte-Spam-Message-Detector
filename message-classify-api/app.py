from flask import Flask, request, jsonify
import gensim.downloader as api
import re
import numpy as np
import spacy
import string
import pickle
import xgboost as xgb

nlp = spacy.load('en_core_web_lg')
wv = api.load("word2vec-google-news-300")

with open("./xgboost_model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

app = Flask(__name__)

def preprocess_and_vectorize(text):
    # clear text
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('\f', '', text)
    # vectorize
    doc = nlp(text)
    filtered_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        filtered_tokens.append(token.lemma_)
    if not filtered_tokens:
        return np.zeros(300)
    return wv.get_mean_vector(filtered_tokens).reshape(1, -1)

@app.route('/', methods=['POST'])
def messageClassify():
    data = request.get_json()
    if 'text' not in data or not isinstance(data['text'], str):
        return jsonify({'error': 'Input must contain a text field as a string'}), 400
    text = data['text']
    print(text)
    prediction = loaded_model.predict(preprocess_and_vectorize(text))
    prediction = 'ham' if prediction else 'spam'
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run()
