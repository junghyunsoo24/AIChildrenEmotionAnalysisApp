from flask import Flask, request
# import pandas as pd
# from tqdm import tqdm
# from konlpy.tag import Okt
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

# okt = Okt()
# dictionary = pd.read_csv('dict.csv')
# list = []
# for word in tqdm(dictionary['word']):
#     list.append(word)

# def getVector(sentence):
#     vector = []
#     tokenized_sentence = okt.morphs(sentence, stem=True) 
#     for token in tokenized_sentence:
#         vector.append(getIndex(token))
#     vector = pad_sequences([vector], maxlen=50)
#     return vector

# def getIndex(sentence):
#     i = 1
#     for word in list:
#         if sentence == word : 
#             return i
#         i = i + 1
#     return 0

# loaded_model = load_model('best_model.h5')
# def predict(sentence) :
#     print(getVector(sentence))
#     return loaded_model.predict(getVector(sentence))
import pandas as pd
from konlpy.tag import Okt
from tqdm import tqdm

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

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
app = Flask(__name__)
 
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
#  InvalidArgumentError
# tensorflow.python.framework.errors_impl.InvalidArgumentError: Graph execution error:
@app.route('/create/', methods=['GET', 'POST'])
def create():
    description = request.form['description']
    emotions = predict(description)
    emotions = emotions[0]
    results = { 
     "plesaure" : str(emotions[0]),
     "anxiety" : str(emotions[1]),
     "sorrow" :str(emotions[2]),
     "embarrassed" : str(emotions[3]),
     "anger" : str(emotions[4]),
     "hurt" : str(emotions[5])
     }
    # for a in emotions:
    #     for emotion in a:
    #         result = result + str(emotion) + ", "
    # result = result + "다음 질문"
    return json.dumps(results)
# def create():
#     result = ""
#     description = request.form['description']
#     emotions = predict(description)
#     for a in emotions:
#         for emotion in a:
#             result = result + str(emotion) + ", "
#     result = result + "다음 질문"
#     html = '''
#         <!doctype html>
#         <html>
#             <head>
#             <title>감정 분류 대화 시스템</title>
#             <meta charset="utf-8">
#             </head>
#             <body>
#             <h1>감정 분류 대화 시스템</h1>
#             <div> '''+ result + '''<div>
#             <form action="/create/" method="POST">
#                 <p><textarea name="description"></textarea></p>
#                 <p><input type="submit"></p>
#             </form>
#             </body>
#         </html>
#         '''
#     return html 
app.run(debug=True) 
# InvalidArgumentError
# tensorflow.python.framework.errors_impl.InvalidArgumentError: Graph execution error:
# The debugger caught an exception in your WSGI application. You can now look at the traceback which led to the error.
# To switch between the interactive traceback and the plaintext one, you can click on the "Traceback" headline. From the text traceback you can also create a paste of it. For code execution mouse-over the frame you want to debug and click on the console icon on the right side.

# You can execute arbitrary Python code in the stack frames and there are some extra helpers available for introspection:

# dump() shows all variables in the frame
# dump(obj) dumps all that's known about the object

# TypeError
# TypeError: Object of type float32 is not JSON serializable