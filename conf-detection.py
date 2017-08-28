import psycopg2
import json 
import pickle
import numpy as np
import time, datetime
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

#-- RELOAD ML MODELS
mnb = MultinomialNB()
mnb = pickle.load( open( "mnb.pkl", "rb" ) )

svectm = SVC()
svectm = pickle.load( open( "svm.pkl", "rb" ) )

knn = KNeighborsClassifier()
knn = pickle.load( open( "knn.pkl", "rb" ) )

#-- OPEN AUDIT DB'
conn = psycopg2.connect(database='audit', user='postgres', password='admin', host='localhost', port='5432', sslmode='prefer')
cur = conn.cursor()

#-- RETRIEVE ALL PATIENTS WHOSE FILE HAS BEEN READ IN PREVIOUS 24 HRS'
patient_query = "select occurrence_date, user_name, patient_id, special_action from audit_event "
patient_query = patient_query + "where audit_event.action_code = 'R' "
patient_query = patient_query + "and occurrence_date > NOW() - INTERVAL '1 day' "
patient_query = patient_query + "and (audit_event.patient_id <> '')  "
patient_query = patient_query + "order by audit_event.user_name asc"

cur.execute(patient_query)

audit_rows = cur.fetchall()

#-- OPEN FHIR DB'
#-- Plv8 engine needs set as the first statement of the connection'
#-- https://github.com/fhirbase/fhirbase-plv8'
fhir_conn = psycopg2.connect(database='fhirbase', user='postgres', password='admin', host='localhost', port='5432', sslmode='prefer')
fhir_cur = fhir_conn.cursor()
fhir_cur.execute("SET search_path to kainos_kingdom_t1,public;")
fhir_cur.execute("SET plv8.start_proc = 'plv8_init';")

print("Run start: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

knn_Acount = 0;knn_Ncount = 0;svm_Acount = 0;svm_Ncount = 0;mnb_Acount = 0;mnb_Ncount = 0

for audit_row in audit_rows:

	occurrenceDate = audit_row[0]
	clinicianID = audit_row[1]
	patientID = audit_row[2]

	if (audit_row[3] is None):
		specialAction = "0"
	else:
		specialAction = "1"	

	#-- OBTAIN APPOINTMENT COUNT'
	fhir_query = "SELECT fhir_search('{\"resourceType\": \"Appointment\", \"queryString\": \"patient=" + patientID + "&practitioner=" + clinicianID + "\"}');"
	# print fhir_query
	fhir_cur.execute(fhir_query)
	fhir_rows = fhir_cur.fetchall()

	' Needed as Postgres returns result as unicode'
	fhir_resource = json.dumps(fhir_rows[0], ensure_ascii=False)

	js = json.loads(fhir_resource)
	appCount = js[0]["total"]

	#-- OBTAIN OBSERVATION COUNT'
	fhir_query = "SELECT fhir_search('{\"resourceType\": \"Observation\", \"queryString\": \"patient=" + patientID + "\"}');"
	# print fhir_query
	fhir_cur.execute(fhir_query)
	fhir_rows = fhir_cur.fetchall()

	' Needed as Postgres returns result as unicode'
	fhir_resource = json.dumps(fhir_rows[0], ensure_ascii=False)

	js = json.loads(fhir_resource)
	obsCount = js[0]["total"]

	#-- OBTAIN ENCOUNTER COUNT'
	fhir_query = "SELECT fhir_search('{\"resourceType\": \"Encounter\", \"queryString\": \"patient=" + patientID + "&practitioner=" + clinicianID + "\"}');"
	# print fhir_query
	fhir_cur.execute(fhir_query)
	fhir_rows = fhir_cur.fetchall()

	' Needed as Postgres returns result as unicode'
	fhir_resource = json.dumps(fhir_rows[0], ensure_ascii=False)

	js = json.loads(fhir_resource)
	encCount = js[0]["total"]

	X = np.array([int(appCount),int(obsCount),int(encCount), int(specialAction)])
	X = X.reshape(1,4)

	#-- PREDICT OBSERVATION CLASS, 'N = Normal, A = Anomalous'
	svm_prediction = svectm.predict(X)
	knn_prediction = knn.predict(X)
	mnb_prediction = mnb.predict(X)
	
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

	print("Clinician: '" + clinicianID  + "' Patient: '" + patientID +   "' Apt/Obs/Enc/BG: "  
	+ str(appCount) + " " + str(obsCount) + " " + str(encCount) + " " +  str(specialAction)
	+ " Prediction: (SVM): " + svm_prediction + " (KNN): " + knn_prediction + " (MNB): " + mnb_prediction)

	#-- RESET COUNTERS
	appCount = ""; obsCount = ""; encCount = ""

print("Run End:   " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")

print "KNN N: " + str(knn_Ncount) + " " +  "A: " + str(knn_Acount) 
print "SVM N: " + str(svm_Ncount) + " " +  "A: " + str(svm_Acount) 
print "MNB N: " + str(mnb_Ncount) + " " +  "A: " + str(mnb_Acount) 

fhir_cur.close()
cur.close()
conn.close()
fhir_conn.close()