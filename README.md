# Cyber incident detection for EMR Systems
Code and data used for MSc in Applied Cyber Security 2017

**Availability Prototype Files**

•	 Data – 3 CSV files were generated from Synthea as part of the prototype, namely:

  o	Normal – containing 16,164 patients (name, address, birthdate, gender, race, ethnicity etc.)

  o	Anomaly - containing 36,447 patients

  o	Combined – a dataset containing 2 x normal and 1 x anomalous set of 68,775 patients.

•	HL7 messages – a zip file containing 68,775 pre-generated A31 HL7 messages.

•	Avail-message-generator.py – a Python file used for generating HL7 messages. At present, this is setup for A31, but could be changed easily to generate other message types or HL7 versions.

•	Avail-detector.py – the detection application which uses Luminol EMA. Outputs a score against each observation.

•	Persistmessage.lua – Lua script used in Iguana to persist messages to a SQLite database.

•	HL7-combined.db – An instance of the SQLite database with 68,775 rows. Each row is a HL7 message that has been passed through Iguana.

•	HL7toDB0.3.vmd – Iguana (Chameleon) file used to map out the database table structure in SQLite. Used within the Iguana Persistmessage.lua script.

**Confidentiality Prototype Files**

•	FHIR Data – appointment (12,000 items), observation (10,800 items), encounter (13,200 items), patient (1200 items) and practitioner (70 items) generated from Velocity Data Loader. 

•	Conf-training.py – Python application used to Train the KNN, SVN and MNB models.

•	Conf-detection.py – Python application used to Test the KNN, SVN and MNB models. Note that the FHIRbase connection string can easily be changed to use an alternative (Non-Evolve IC) installation, providing the means for future research to continue without an Evolve IC dependency.

•	Models – the persisted ‘pickled’ versions of the trained KNN, SVM and MNB used in testing.
