import pandas as pd
import numpy as np
import sys
import scipy
import matplotlib
import sklearn
from datetime import datetime

icustay = pd.read_csv("ICUSTAYS.csv.gz")
admissions = pd.read_csv("ADMISSIONS.csv.gz")
d_items = pd.read_csv("D_ITEMS.csv.gz")
diagnoses = pd.read_csv("DIAGNOSES_ICD.csv.gz")
d_diagnoses = pd.read_csv("D_ICD_DIAGNOSES.csv.gz")
patients = pd.read_csv("PATIENTS.csv.gz")

#import matplotlib.pyplot as plt

icuList = icustay['SUBJECT_ID'];


pneumAdmitIDS = admissions[admissions['DIAGNOSIS'].str.contains("PNEUMONIA") == True]['HADM_ID']

#print(icuList.head())
pneumAdmitIDS = pneumAdmitIDS.reset_index()
pneumAdmitIDS = pneumAdmitIDS.drop(columns='index')
        


columns = ["SUBJECT_ID","AGE", "BEHAVIOR", "BODY_TEMP", "BUN",  "CREATININE",  "GENDER", "GLUCOSE", "HEIGHT", "HEMATOCRIT", "HR",
            "RR", "SODIUM", "SP_O2", "SYST_BP", "TOBACCO_HIST", "WBC_COUNT", "WEIGHT", "LOS"]


# print(pneumAdmitIDS)



# print("BAD ",pneumAdmitIDS.loc[0,'SUBJECT_ID'])

# print(357 in icuList)

        

#need to connect DOB (on SubjectId) with ADMITTIME (on HadmId)
patientData = pd.DataFrame(index=pneumAdmitIDS['HADM_ID'], columns=columns)



#print(patientData.head())




for subject in pneumAdmitIDS['HADM_ID']:
    sid = admissions.loc[admissions['HADM_ID'] == subject]['SUBJECT_ID']
    sid = sid.to_frame();
    patientData.loc[subject, 'SUBJECT_ID'] =sid.iloc[0]['SUBJECT_ID']
    
i = 0

while i < len(patientData):

    if patientData.iloc[i, 0] not in icuList:
        #print(pneumAdmitIDS.iloc[i,0])
        patientData = patientData.drop(patientData.index[i])
    else:
        i = i+1
        

 

#print(patientData.head())

for admit in patientData.index.values.tolist():
    sID = patientData.loc[admit,'SUBJECT_ID']
    admDate = admissions[admissions['HADM_ID'] == admit]['ADMITTIME'].iloc[0]
    DOB = patients[patients['SUBJECT_ID'] == sID]['DOB'].iloc[0]
    
    admDate = datetime.strptime(admDate, "%Y-%m-%d %H:%M:%S%f")
    DOB = datetime.strptime(DOB, "%Y-%m-%d %H:%M:%S%f")
    
    admM = admDate.month
    DOBM = DOB.month
    
    admY = admDate.year
    DOBY = DOB.year
    
    age = admY-DOBY
    
    if admM < DOBM:
        age = age-1
    
    if age > 200:
        age = 89
    
    patientData.loc[admit,'AGE'] = age
    
    gender = patients[patients['SUBJECT_ID'] == sID]['GENDER'].iloc[0]
    patientData.loc[admit,'GENDER'] = gender


print(patientData['AGE'].head())
        




#print(icustay[icustay['HADM_ID'] == 101651])
# print(pneumAdmitIDS.head())


for i in range(0, len(patientData.index.values.tolist())):
    subject = patientData.index.values.tolist()[i]
    tmp = icustay[icustay['HADM_ID'] == subject]['LOS'].sum()
    patientData.loc[subject, 'LOS'] = tmp

# print("PNEUMPATIENTS: ",pneumAdmitIDS.shape[0])
chunksize = 10 ** 6
count = 0


# assign each parameter an index. use to update rows in patientEvents
dItemIds = {226105:0, 223761:1, 225624:2, 220615:3, 811:4, 226730:5, 813:6, 220045:7, 618:8, 837:9, 646:10, 220179:11, 227687:12, 220546:13, 226531:14}

#for subject in pneumAdmitIDS['SUBJECT_ID']:
  #  patientData.loc[subject,'AGE'] = admissions.loc[subject,'ADMITTIME'] - patients.loc[subject,'DOB']

# USING ROW_ID
# #2339 = NOS Leukemia in Relapse
# #8980 = fever NOS
# #4369 = old myocard infarc
# #4476 = acute systolic hf
# #11403 = sepsis
# #5123 = chronic airway obstruct (NEC)
# #5916 = renal failure NOS
# #55299 = influenza with pneumonia
# #14474 = screen-diabetes mellitus

#dDiagtoString = {'2339':"LEUKEMIA", '8980':"FEVER", '4369':"OLD_HATTACK", '4476': "AC_SYST_HF", '11403': "SEPSIS", '5123': "CHRONIC_AIRWAY_OBS",'5916': "RENAL_FAIL", '55299': "FLU_W_PNEUMONIA", '14474': "DIABETES"}
# assign each parameter a string. use to update corresponding columns in patientData later on            
dItemtoString = {226105:"BEHAVIOR", 223761:"BODY_TEMP", 225624:"BUN", 220615:"CREATININE", 811: "GLUCOSE", 226730: "HEIGHT", 813:"HEMATOCRIT",
                 220045: "HR", 618: "RR", 837:"SODIUM", 646:"SPO2", 220179:"SYST_BP", 227687:"TOBACCO_HIST", 220546:"WBC_COUNT", 226531:"WEIGHT"}

#dDiag = ['2339', '8980', '4369', '4476', '11403', '5123', '5916', '55299', '14474']

dItems = [226105, 223761, 225624, 220615, 811, 226730, 813, 220045, 618, 837, 646, 220179, 227687 , 220546 , 226531]

# all of the earliest measurements for each patient
# index 0 is the itemid
# index 1 is the earliest instance
# index 2 is the measured value
# patientEvents = np.zeros((len(pneumAdmitIDS), len(dItemIds), 3));
patientEvents = [[['', ''] for i in range(len(dItemIds))] for j in range(len(patientData.index.values.tolist()))]

# fill index zero for all patients with the different parameter ids. 
# for patient in patientEvents:
#    for parameter in patient:
#        parameter[0] = dItems[count]
#        count = count + 1
#    count = 0
    
# assign each patient a number (dictionary). use it to update their row in patientData later on.
count = 0
patientIds = {};
for patient in patientData.index.values.tolist():
    patientIds[patient] = count;
    count = count + 1;
    
    




# iterate through CHARTEVENTS. If a row has information about the current patient, check if it's information we want
# if it's info we want, check if it's earlier than the last instance of that info. if so, update in patientEvents. 
count = 0
for miniCEvents in pd.read_csv("CHARTEVENTS.csv.gz", chunksize=chunksize):
    for row in miniCEvents.itertuples():
        if row[5] in dItemIds:
            for subject in patientData.index.values.tolist():
                if row[3] == subject:
                    #patientEvents[patientIds[subject]]
                    
                    if row[6] < patientEvents[patientIds[subject]][dItemIds[row[5]]][0] or patientEvents[patientIds[subject]][dItemIds[row[5]]][0] == '':
                        patientEvents[patientIds[subject]][dItemIds[row[5]]][0] = row[6]
                        patientEvents[patientIds[subject]][dItemIds[row[5]]][1] = row[9]
                        break
                



    

#print(diagnoses.head())

#icd9s = d_diagnoses['ICD9_CODE'];

#print(d_diagnoses.columns)
#print(d_diagnoses[d_diagnoses['ROW_ID'] == 2339]['ICD9_CODE'])

#for row in diagnoses.itertuples():  # didn't test this loop
   # if row[5] in dDiag:
      #  for subject in pneumAdmitIDS['SUBJECT_ID']:
          #  if row[2] == subject:
            #    print("YAY")
               # patientData.loc[subject, dDiagtoString[row[5]]] = True

# print(patientData[patientData["DIABETES"] == True])


# iterate through patientEvents using patientIds dictionary. transfer each value to patientData      
for subject in patientData.index.values.tolist():
    for item in dItems:
        patientData.loc[subject, dItemtoString[item]] = patientEvents[patientIds[subject]][dItemIds[item]][1]
       # print(patientData.loc[pneumAdmitIDS.loc[i,'SUBJECT_ID'],dItemtoString[int(parameter[0])]])

    

# "BEHAVIOR", "BODY_TEMP", "BUN",  "CREATININE",  "GENDER", "GLUCOSE", "HEIGHT", "HEMATOCRIT", "HR",
     #       "RR", "SODIUM", "SP_O2", "SYST_BP", "TOBACCO_HIST", "WBC_COUNT", "WEIGHT", "LOS"
    
patientData.fillna(patientData.mean())

patientData.to_csv('/Users/mirakraju/Desktop/patientData.csv')


# print(icustay.head());
# print(icustay.iloc[357])
# print(patientData.head())

# for i in range(0, len(pneumAdmitIDS)):
#    patient = pneumAdmitIDS.loc[i, 'SUBJECT_ID']
#    LOS = icustay.iloc[patient]['LOS']
#    break;

# print(patientData.iloc[0,0])
    
#-----------------------------------------------------------------------------------------------------------------------------------------
# LOS
# print(list(d_items.columns.values))
# print(admissions[admissions['DIAGNOSIS'].str.contains("PNEUMONIA")== True])

# print("Number of Pneumonia Admissions: "+ str(pneumAdmitIDS.shape[0]))

# spread: whether it's unilobar or multilobar
# 33

# print(patientData.head())

# print(d_items[d_items['ITEMID'] == 646]) #heart rate!!
# print("height") 12304
# print(d_items[d_items['ITEMID'] == 227687])
# print(d_diagnoses[2615:2616]['ROW_ID'])#['SHORT_TITLE'])

# print(d_items[d_items['LABEL'].str.contains("Gender")==True]['ITEMID'])
#print(d_diagnoses[d_diagnoses['SHORT_TITLE'].str.contains("neumonia")]['SHORT_TITLE'])
#print(d_diagnoses[d_diagnoses['SHORT_TITLE'].str.contains("neumonia")]['ICD9_CODE'])

# In D_ITEMS:
# 226730 = height cm
# 226531 = admission weight lbs
# 227860 = resting resp rate
# 220615 = creatinine
# 225624 = BUN
# 220045 = HR
# 223761 = Body Temp (F)
# 646    = SpO2
# 226228 = Gender
# age = 226984
# 220546 = WBC count
# 227687 = Tobacco Use History

# 226534 = sodium (whole blood)
# 811    = glucose (70-105)
# 3761   = hematocrit (35-51)
# 220179 = non-invasive systolic blood pressure
# 226105 = behavior

# In D_DIAGNOSES:
# uncertain of which cancer to use... if at all
# Thinking about leukemia and lymphoma
# USING ROW_ID
# #2339 = NOS Leukemia in Relapse
# #8980 = fever NOS
# #4369 = old myocard infarc
# #4476 = acute systolic hf
# #11403 = sepsis
# #5123 = chronic airway obstruct (NEC)
# #5916 = renal failure NOS
# #55299 = influenza with pneumonia
# #14474 = screen-diabetes mellitus
