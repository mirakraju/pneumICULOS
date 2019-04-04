#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 00:04:59 2018

@author: mirakraju
"""

import pandas as pd
import numpy as np
import sys
import scipy
import matplotlib
import sklearn
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense

icustay = pd.read_csv("ICUSTAYS.csv.gz")
admissions = pd.read_csv("ADMISSIONS.csv.gz")
d_items = pd.read_csv("D_ITEMS.csv.gz")
diagnoses = pd.read_csv("DIAGNOSES_ICD.csv.gz")
d_diagnoses = pd.read_csv("D_ICD_DIAGNOSES.csv.gz")
patients = pd.read_csv("PATIENTS.csv.gz")

dItems = [226105, 223761, 225624, 220615, 811, 226730, 813, 220045, 6749, 837, 646, 3313, 227687 , 220546 , 226531]

for i in range(0,len(dItems)):
    print(dItems[i])
    item = dItems[i]
    print(d_items[d_items['ITEMID'] == item]['LABEL']) #heart rate!!
# print("height") 12304
# print(d_items[d_items['ITEMID'] == 227687])
# print(d_diagnoses[2615:2616]['ROW_ID'])#['SHORT_TITLE'])

print(d_items[d_items['LABEL'].str.contains("Blood Pressure")==True]['ITEMID'])
print(d_items[d_items['LABEL'].str.contains("Blood Pressure")==True]['LABEL'])
#print(d_diagnoses[d_diagnoses['SHORT_TITLE'].str.contains("neumonia")]['SHORT_TITLE'])
#print(d_diagnoses[d_diagnoses['SHORT_TITLE'].str.contains("neumonia")]['ICD9_CODE'])
