import pandas
import pickle
import numpy as np

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn import tree

# READ IN TRAINING DATA
Training_CSV = 'conf-evolveic-3anom.csv'
columns = ['Appointments', 'Observations', 'Encounters', 'SpecialAction']
df = pandas.read_csv(Training_CSV, names=columns)

knn = KNeighborsClassifier()
knn = pickle.load( open( "knn.pkl", "rb" ) )

svectm = SVC()
svectm = pickle.load( open( "svm.pkl", "rb" ) )

mnb = MultinomialNB()
mnb = pickle.load( open( "mnb.pkl", "rb" ) )

crt = tree.DecisionTreeClassifier()
crt = pickle.load( open( "crt.pkl", "rb" ) )

knn_Acount = 0;knn_Ncount = 0;svm_Acount = 0;svm_Ncount = 0;mnb_Acount = 0;mnb_Ncount = 0;crt_Acount = 0;crt_Ncount = 0

for index, row in df.iterrows():
    X = np.array([int(row['Appointments']),int(row['Observations']),int(row['Encounters']), int(row['SpecialAction'])])
    X = X.reshape(1,4)

    knn_prediction = knn.predict(X)
    svm_prediction = svectm.predict(X)
    mnb_prediction = mnb.predict(X)
    crt_prediction = crt.predict(X)

    if knn_prediction[0] == "A":
        knn_Acount = knn_Acount + 1
    else:
        knn_Ncount = knn_Ncount + 1

    if svm_prediction[0] == "A":
        svm_Acount = svm_Acount + 1
    else:
        svm_Ncount = svm_Ncount + 1

    if mnb_prediction[0] == "A":
        mnb_Acount = mnb_Acount + 1
    else:
        mnb_Ncount = mnb_Ncount + 1

    if crt_prediction[0] == "A":
        crt_Acount = mnb_Acount + 1
    else:
        crt_Ncount = mnb_Ncount + 1

    print "Row " + str(X) + " Prediction: " + str(knn_prediction) + " " + str(svm_prediction) + " " + str(mnb_prediction) + " " + str(crt_prediction) 
print "KNN N: " + str(knn_Ncount) + " " +  "A: " + str(knn_Acount) 
print "SVM N: " + str(svm_Ncount) + " " +  "A: " + str(svm_Acount) 
print "MNB N: " + str(mnb_Ncount) + " " +  "A: " + str(mnb_Acount) 
print "CRT N: " + str(crt_Ncount) + " " +  "A: " + str(crt_Acount) 