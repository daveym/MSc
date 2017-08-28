from time import gmtime, strftime
from datetime import datetime

import os
import pandas as pd
import numpy as np

OUTPUTDIR = "hl7"

df = pd.read_csv('payload-normal.csv')

i=0
for index, row in df.iterrows():

    # MESSAGE HEADER - http://www.hl7.eu/refactored/segMSH.html
    msh = "MSH|"
    msh = msh + "^~\&|"
    msh = msh + "AcmePAS|"                                                 # Sending Application
    msh = msh + 'St. Johns|'                                               # Sending Facility
    msh = msh + 'AcmeEMR|'                                                 # Receiving Application
    msh = msh + 'St. Lukes|'                                               # Receiving Facility

    msh = msh + datetime.now().strftime('%Y%m%d%H%M%S') + "||"             # Date/Time of Message 
    msh = msh + str(df.loc[index]['MSGTYPE']) + "|"                        # Message Type
    msh = msh + str(df.loc[index]["MSGCTRLID"]) + "|"                      # Message Control ID
    msh = msh + "P|"                                                       # Production Flag
    msh = msh + "2.3|" + "\n"                                              # Version
    
    # EVENT - http://www.hl7.eu/refactored/segEVN.html#10
    evn = "EVN|A01|"
    evn = evn + datetime.now().strftime('%Y%m%d%H%M%S')  + "|" + "\n"      # Event Date
    
    # PATIENT ID - http://www.hl7.eu/refactored/segPID.html
    pid = "PID|||"
    pid = pid + str(df.loc[index]['PATIENTID']) + "||"              # Patient ID
    pid = pid + str(df.loc[index]['LAST']) + "^"                    # Lastname
    pid = pid + str(df.loc[index]['FIRST']) + "||"                  # Firstname
    pid = pid + str(df.loc[index]['BIRTHDATE']) + "|"               # DOB
    pid = pid + str(df.loc[index]['GENDER']) + "|||"                # SEX
    pid = pid + str(df.loc[index]['ADDRESS']) + "||||||||" + "\n"   # ADDRESS
    
    # PATIENT VISIT - http://www.hl7.eu/refactored/segPV1.html      # Patient Class
    pv1 = "PV1||" 
    pv1 = pv1 + "I|" + "\n"
    
    s = msh + evn + pid + pv1

    if not os.path.exists(OUTPUTDIR):
        os.makedirs(OUTPUTDIR)

    with open("./" + OUTPUTDIR + "/" + str(index) + ".hl7", "w") as hl7file:
        hl7file.write(s)
        
print ("\nHL7 Files Written successfully to " + OUTPUTDIR + " directory.")