import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignoreLetters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = nltk.word.tokenize(pattern)
        words.entend(wordList)
        documents.append((wordList, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    for word in words: 
        if word in wordPatterns:
            bag.append(1) 
        else:
            bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)

random.shuffle(training)
training = np.array(training)

trainX = training[:, :len(words)]
trainY = training[:, len(words):]

model = tf.keras.Sequential()
model.add(tf.keras.layer.Dense(128, input_shape = (len(trainX[0]),),activation = 'relu'))
model.add(tf.keras.layer.Dropout(0.5))
model.add(tf.keras.layer.Dense(64,activation = 'relu'))
model.add(tf.keras.layer.Dense(len(trainY[0]), activation = 'softmax'))
          
sgd = tf.keras.optimizers.SGD(learning_rate = 0.01, momentum = 0.9, nesterov = True)

model.complile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])
hist = model.fit(np.array(trainX), np.array(trainY), epochs = 200, batch_size = 5, verbose = 1)
model.save('chatbot_simple_linear_model.h5', hist)
print("Executed Successfully")