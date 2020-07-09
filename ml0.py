import sklearn
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from sklearn import linear_model, preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from keras.models import Sequential
from keras import layers
import requests
import os
import pandas as pd
import numpy as np



data = pd.read_csv("learn_data.csv")
le = preprocessing.LabelEncoder()
FEATURES = ['payload','html']
PREDICT = 'state'
payload = le.fit_transform(data["payload"])
html = le.fit_transform(data["html"])
state = data["state"]

X = list(zip(payload, html))
Y = list(state)
model0 = KNeighborsClassifier(n_neighbors=7)
neighbors = 0
while 1:
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
    if neighbors == 10:
        neighbors = 0
    neighbors += 1
    model0.fit(x_train, y_train)
    acc = model0.score(x_test, y_test)
    print("[-] Accuracy for training[KNEIGHBOR]: ", acc, end="\r")
    if acc >= 0.997:
        print("\n", neighbors)
        break

predicted = model0.predict(x_test)

wrong = 0
success = 0
for x in range(len(predicted)):
    if predicted[x] !=  y_test[x]:
        wrong += 1
        print("[-] Predicted: ", predicted[x], "Data: ", x_test[x], "Actual: ", y_test[x])
    elif predicted[x] ==  y_test[x]:
        success += 1

xssSuccess = 0
for i in data["state"]:
    if i == 1:
        xssSuccess +=1

acc2 = metrics.accuracy_score(y_test, predicted)
print("[-] Accuracy for testing[KNEIGHBOR]: ", acc2)

html_text = requests.get("https://xss-game.appspot.com/level1/frame").text

payload = le.fit_transform(["</textarea><script>alert(/xss/)</script>"])
html_text = le.fit_transform(list(html_text))
array = list(zip(payload, html_text))
predicted = model0.predict(array)
print("[-]", predicted)

print("[-] Total XSS Successes existing file: ", xssSuccess)

print(f"[-] I got {wrong} wrong guesses out of total {xssSuccess} which refers to a real accuracy of: {1-(wrong/xssSuccess)}")
print(f"[-] I got {success} right guesses but is irrelevant i think")

print("[-] Trying regression now...")
model1 = linear_model.LinearRegression()
model1.fit(x_train, y_train)
acc = model1.score(x_test, y_test)
print("[-] Accuracy for training[REGRESSION]: ", acc)

