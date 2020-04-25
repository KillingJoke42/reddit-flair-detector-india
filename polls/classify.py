from csv import reader
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

from sklearn import preprocessing
import joblib

import numpy as np
from numpy import array
from numpy import asarray
from numpy import zeros
import re
import nltk
from nltk.corpus import stopwords
from tensorflow.keras import models, layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+,_\"]')
STOPWORDS = set(stopwords.words('english'))

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def preprocess_text(text):
    text = text.lower()
    text = remove_tags(text)
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def prepare_train_data():
	X_train = list()
	y_train_text = list()

	get_metric = dict()

	with open('hot/flair_dataset.csv') as csv_file:
		csv_reader = reader(csv_file, delimiter=',', quotechar='"')
		for row in csv_reader:
			if row[1] != '':
				if row[1] in get_metric.keys():
					get_metric[row[1]] += 1
				else:
					get_metric[row[1]] = 1
				X_train.append(preprocess_text(row[0]))
				y_train_text.append(row[1])

	X_train = np.array(X_train)
	y_train_text = np.array([[flair] for flair in y_train_text])
	y_train = dict()
	y_train_vectored = list()
	countVector = 0
	for i in range(y_train_text.shape[0]):
		label = y_train_text[i][0]
		if label not in y_train.keys():
			y_train[label] = countVector
			y_train_vectored.append(countVector)
			countVector += 1
		else:
			y_train_vectored.append(y_train[label])
	y_train_vectored = np.array(y_train_vectored)
	return X_train, y_train_text, y_train_vectored, y_train

X_train, y_train_text, y_train_vectored, y_train = prepare_train_data()

def ml_train(model_type):
	
	if model_type == "baye":
		print(y_train)
		classifier = Pipeline([
			('vectorizer', CountVectorizer()),
			('tfidf', TfidfTransformer()),
			('clf', MultinomialNB())])
		classifier.fit(X_train, y_train_vectored)
		filename = 'native_baye.sav'
		joblib.dump(classifier, filename)

	elif model_type == "sgd":
		print(y_train)
		classifier = Pipeline([
			('vectorizer', CountVectorizer()),
			('tfidf', TfidfTransformer()),
			('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None))])
		classifier.fit(X_train, y_train_vectored)
		filename = 'sgd.sav'
		joblib.dump(classifier, filename)

	elif model_type == "regression":
		print(y_train)
		classifier = Pipeline([
			('vectorizer', CountVectorizer()),
			('tfidf', TfidfTransformer()),
			('clf', LogisticRegression(n_jobs=1, C=1e5, max_iter=10000))])
		classifier.fit(X_train, y_train_vectored)
		filename = 'regression.sav'
		joblib.dump(classifier, filename)

	elif model_type == "random_forrest":
		print(y_train)
		classifier = Pipeline([
			('vectorizer', CountVectorizer()),
			('tfidf', TfidfTransformer()),
			('clf', RandomForestClassifier(n_estimators = 1000, random_state = 42))])
		classifier.fit(X_train, y_train_vectored)
		filename = 'random_forrest.sav'
		joblib.dump(classifier, filename)

	elif model_type == "all":
		ml_train("baye")
		ml_train("sgd")
		ml_train("regression")
		ml_train("random_forrest")

def classify(classifier, text):
	X_test = np.array([preprocess_text(text)])
	predicted = classifier.predict(X_test)
	return predicted

#ml_train("all")