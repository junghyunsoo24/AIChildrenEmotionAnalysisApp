# import pandas as pd
# import matplotlib.pyplot as plt
# from gensim.models.word2vec import Word2Vec
# from konlpy.tag import Okt
# from tqdm import tqdm
# import tensorflow as tf

# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.layers import Embedding, Dense, LSTM
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import load_model
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# from tensorflow.keras.layers import SimpleRNN

# okt = Okt()

#==================== 여기만 ppt에서 링크 코드 수정하면 됨 + 데이터 셋 엑셀 파일을 csv파일로 + 라벨 변환===================================
train_data = pd.read_csv('X_train_binary.csv')
test_data = pd.read_csv('X_test_binary.csv')

# print('훈련용 리뷰 개수 :',len(train_data)) # 훈련용 리뷰 개수 출력
# print('테스트용 리뷰 개수 :',len(test_data)) # 훈련용 리뷰 개수 출력

# train_data[:5] # 상위 5개 출력
# test_data[:5]

# train_data['document'].nunique(), train_data['label'].nunique() # document 열의 중복 제거
# train_data.drop_duplicates(subset=['document'], inplace=True)
# print('총 샘플의 수 :',len(train_data))
# print(train_data.groupby('label').size().reset_index(name = 'count'))
# train_data['label'].value_counts().plot(kind = 'bar')

# # 한글과 공백을 제외하고 모두 제거
# train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
# train_data[:5]

# test_data.drop_duplicates(subset = ['document'], inplace=True) # document 열에서 중복인 내용이 있다면 중복 제거
# test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
# print('전처리 후 테스트용 샘플의 개수 :',len(test_data))

# stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

# X_train = []
# for sentence in tqdm(train_data['document']):
#     tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
#     stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
#     X_train.append(stopwords_removed_sentence)

# X_test = []
# for sentence in tqdm(test_data['document']):
#     tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
#     stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
#     X_test.append(stopwords_removed_sentence)


# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(X_train)

# threshold = 3
# total_cnt = len(tokenizer.word_index) # 단어의 수
# rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
# total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
# rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
# for key, value in tokenizer.word_counts.items():
#     total_freq = total_freq + value

#     # 단어의 등장 빈도수가 threshold보다 작으면
#     if(value < threshold):
#         rare_cnt = rare_cnt + 1
#         rare_freq = rare_freq + value

# print('단어 집합(vocabulary)의 크기 :',total_cnt)
# print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
# print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
# print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)
# # 전체 단어 개수 중 빈도수 2이하인 단어는 제거.
# # 0번 패딩 토큰을 고려하여 + 1
# vocab_size = total_cnt - rare_cnt + 1
# print('단어 집합의 크기 :',vocab_size)

# tokenizer = Tokenizer(vocab_size) 
# tokenizer.fit_on_texts(X_train)
# X_train = tokenizer.texts_to_sequences(X_train)
# X_test = tokenizer.texts_to_sequences(X_test)
# print(X_train[:3])
# print(X_test[:3])

# import numpy as np
# y_train = np.array(train_data['label'])
# y_test = np.array(test_data['label'])

# print('발화의 최대 길이 :',max(len(review) for review in X_train))
# print('발화의 평균 길이 :',sum(map(len, X_train))/len(X_train))
# plt.hist([len(review) for review in X_train], bins=50)
# plt.xlabel('length of samples')
# plt.ylabel('number of samples')
# plt.show()

# def below_threshold_len(max_len, nested_list):
#   count = 0
#   for sentence in nested_list:
#     if(len(sentence) <= max_len):
#         count = count + 1
#   print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (count / len(nested_list))*100))

# max_len = 50
# below_threshold_len(max_len, X_train)

# X_train = pad_sequences(X_train, maxlen=max_len)
# X_test = pad_sequences(X_test, maxlen=max_len)

# print(X_test[:5])
# print(y_test[:5])
# print(X_test.size)
# print(y_test.size)
# print(vocab_size)

# embedding_dim = 100
# hidden_units = 128

# model = Sequential()
# model.add(Embedding(vocab_size, embedding_dim))
# model.add(LSTM(hidden_units))
# model.add(Dense(1, activation='sigmoid'))

# es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
# mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

# model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
# history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=64, validation_split=0.2)
# loaded_model = load_model('best_model.h5')
# print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))
# # model.add(Dense(8, kernel_initializer = 'uniform', activation = 'relu'))
# # model.add(Dense(8, kernel_initializer = 'uniform', activation = 'relu'))
# # model.add(Dense(8, kernel_initializer = 'uniform', activation = 'relu'))
# # model.add(Dense(1, activation='sigmoid'))

# # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# # history = model.fit(X_train, y_train, epochs=200, batch_size=128, validation_data=(X_test, y_test))
# # epochs = range(1, len(history.history['accuracy']) + 1)
# # plt.plot(epochs, history.history['loss'])
# # plt.plot(epochs, history.history['val_loss'])
# # plt.title('model loss')
# # plt.ylabel('loss')
# # plt.xlabel('epoch')
# # plt.legend(['train', 'val'], loc='upper left')
# # plt.show()

# model.save("LSTM_binary_sigmoid_model.h5")
# model = load_model("LSTM_binary_sigmoid_model.h5")
# def sentiment_predict(new_sentence):
#   new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
#   new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
#   encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
#   pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
#   score = float(model.predict(pad_new)) # 예측
#   if(score > 0.83):
#     print("{:.2f}% 확률로 부정 반응입니다.\n".format(score * 100))
#   else:
#     print("{:.2f}% 확률로 긍정 반응입니다.\n".format((1 - score) * 100))

# sentiment_predict('나한테 잘해')