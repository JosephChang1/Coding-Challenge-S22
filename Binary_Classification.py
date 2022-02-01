# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 22:48:29 2022

@author: josep
"""
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#load data
dataset  = pd.read_csv('mushrooms.csv')
#pd.set_option('display.max_columns', 30)
X = dataset.iloc[:, 1:].values
y = dataset.iloc[:, 0].values

# train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=21)
#print('Train', X_train.shape, y_train.shape)
#print('Test', X_test.shape, y_test.shape)

# prepare input data, encode variables into integers
oe = OrdinalEncoder()
oe.fit(X_train)
X_train_enc = oe.transform(X_train)
X_test_enc = oe.transform(X_test)

# prepare target variable, encode target variables into integers (0 or 1)
le = LabelEncoder()
le.fit(y_train)
y_train_enc = le.transform(y_train)
y_test_enc = le.transform(y_test)

# feature selection
fs = SelectKBest(score_func=chi2, k='all')
fs.fit(X_train_enc, y_train_enc)
X_train_fs = fs.transform(X_train_enc)
X_test_fs = fs.transform(X_test_enc)
for i in range(len(fs.scores_)):
	print('Feature %d: %f' % (i, fs.scores_[i]))
    
# plot the scores
plt.bar([i for i in range(len(fs.scores_))], fs.scores_)
plt.show()

# fit the model
model = LogisticRegression(solver='lbfgs', max_iter=10000)
model.fit(X_train_enc, y_train_enc)

# evaluate the model
yhat = model.predict(X_test_enc)

# evaluate predictions
accuracy = accuracy_score(y_test_enc, yhat)
print('Accuracy: %.2f' % (accuracy*100))
#print(yhat)
#print(y_test_enc)
