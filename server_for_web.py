from flask import Flask, request
import json
import pandas as pd
from konlpy.tag import Okt
from tqdm import tqdm

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
app = Flask(__name__)


okt = Okt()

train_data = pd.read_csv('X_train.csv')
test_data = pd.read_csv('X_test.csv')

train_data['document'].nunique(), train_data['label'].nunique() 
train_data.drop_duplicates(subset=['document'], inplace=True)
train_data['label'].value_counts().plot(kind = 'bar')

train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

test_data.drop_duplicates(subset = ['document'], inplace=True) 
test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") 
print('전처리 후 테스트용 샘플의 개수 :',len(test_data))

stopwords = ['']

X_train = []
for sentence in tqdm(train_data['document']):
    tokenized_sentence = okt.morphs(sentence, stem=True) 
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] 
    X_train.append(stopwords_removed_sentence)

X_test = []
for sentence in tqdm(test_data['document']):
    tokenized_sentence = okt.morphs(sentence, stem=True) 
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] 
    X_test.append(stopwords_removed_sentence)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

total_cnt = len(tokenizer.word_index) 
rare_cnt = 0 

vocab_size = total_cnt - rare_cnt + 1

tokenizer = Tokenizer(vocab_size) 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

loaded_model = load_model('best_model.h5')
def predict(sentence) :
    sentence = okt.morphs(sentence, stem=True) 
    x_test = tokenizer.texts_to_sequences([sentence])

    x_test = pad_sequences(x_test, maxlen=50)
    return loaded_model.predict(x_test)
print("안녕") 
 
@app.route('/')
def index():
    html = '''
        <!doctype html>
        <html>
            <head>
            <title>감정 분류 대화 시스템</title>
            <meta charset="utf-8">
            </head>
            <body>
            <h1>감정 분류 대화 시스템</h1>
            <div> '''+ '질문' +'''<div>
            <form action="/create/" method="POST">
                <p><textarea name="description"></textarea></p>
                <p><input type="submit"></p>
            </form>
            </body>
        </html>
        '''
    return html

@app.route('/create/', methods=['GET', 'POST'])
def create():
    result = ""
    description = request.form['description']
    emotions = predict(description)
    for a in emotions:
        for emotion in a:
            result = result + str(emotion) + ", "
    result = result + "다음 질문"
    html = '''
        <!doctype html>
        <html>
            <head>
            <title>감정 분류 대화 시스템</title>
            <meta charset="utf-8">
            </head>
            <body>
            <h1>감정 분류 대화 시스템</h1>
            <div> '''+ result + '''<div>
            <form action="/create/" method="POST">
                <p><textarea name="description"></textarea></p>
                <p><input type="submit"></p>
            </form>
            </body>
        </html>
        '''
    return html 

app.run(debug=True) 