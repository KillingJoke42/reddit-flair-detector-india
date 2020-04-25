#import classify
from classify import classify as clf, preprocess_text, y_train
import csv
import numpy as np
import joblib

def get_acc(classifier):

	X_test = list()
	y_test = list()

	with open('new/flair_dataset.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',', quotechar='\"')
		for row in csv_reader:
			X_test.append(preprocess_text(row[0]))
			y_test.append(row[1])

	X_test = np.array(X_test)
	y_test = np.array(y_test)

	correct = 0
	count_blank = 0
	keys_new = list()
	for i in range(len(X_test)):
		pred = clf(classifier, X_test[i])
		try:
			if pred == y_train[y_test[i]]:
				correct += 1
			else:
				pass
		except KeyError:
			keys_new.append(y_test[i])
			count_blank += 1

	accuracy = (correct / len(X_test)) * 100
	return accuracy

classifier = joblib.load('native_baye.sav')
print("Native Bayes: " + str(get_acc(classifier)))
classifier = joblib.load('random_forrest.sav')
print("Random Forrest: " + str(get_acc(classifier)))
classifier = joblib.load('regression.sav')
print("Logistic Regression: " + str(get_acc(classifier)))
classifier = joblib.load('sgd.sav')
print("Linear SVM: " + str(get_acc(classifier)))