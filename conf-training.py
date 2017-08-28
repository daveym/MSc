import pandas
import pickle
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
from sklearn.svm import SVC

K_SPLITS = 7;VALIDATION_SIZE = 0.34

# READ IN TRAINING DATA
Training_CSV = 'conf-training-dataset.csv'
columns = ['User_name', 'PatientID', 'Appointments', 'Observations', 'Encounters', 'SpecialAction', 'Class']
df = pandas.read_csv(Training_CSV, names=columns)

# SPLIT TRAINING/VALIDATION
array = df.values
X = array[:,2:6]
Y = array[:,6]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=VALIDATION_SIZE)

models = []
models.append(('KNN', KNeighborsClassifier()))
models.append(('SVM', SVC()))
models.append(('MNB', MultinomialNB()))
models.append(('CRT', tree.DecisionTreeClassifier()))

# EVALUATE MODELS
for name, model in models:
	kfold = KFold(n_splits=K_SPLITS)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	print(name, cv_results.mean(), cv_results.std())

# FIT AND PERSIST MODELS FOR DETECTION
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
knn_predict = knn.predict(X_test)
report = classification_report(Y_test, knn_predict)
print "\nKNN"; print report

output = open('knn.pkl', 'wb')
pickle.dump(knn, output)
output.close()

svectm = SVC()
svectm.fit(X_train, Y_train)
svm_predict = svectm.predict(X_test)
report = classification_report(Y_test, svm_predict)
print "SVM"; print report

output = open('svm.pkl', 'wb')
pickle.dump(svectm, output)
output.close()

mnb = MultinomialNB()
mnb.fit(X_train, Y_train)
mnb_predict = mnb.predict(X_test)
report = classification_report(Y_test, mnb_predict)
print "MNB"; print report

output = open('mnb.pkl', 'wb')
pickle.dump(mnb, output)
output.close()


crt = tree.DecisionTreeClassifier()
crt.fit(X_train, Y_train)
crt_predict = crt.predict(X_test)
report = classification_report(Y_test, crt_predict)
print "CRT"; print report

output = open('crt.pkl', 'wb')
pickle.dump(crt, output)
output.close()