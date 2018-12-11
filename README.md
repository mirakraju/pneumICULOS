# pneumICULOS
Code for a machine learning model predicting the length of stay for pneumonia patients in the ICU. 

This model makes use of MIMIC-III, a freely accessible critical care database. Johnson AEW, Pollard TJ, Shen L, Lehman L, Feng M, Ghassemi M, Moody B, Szolovits P, Celi LA, and Mark RG. Scientific Data (2016). DOI: 10.1038/sdata.2016.35. 

The code requires tables from the MIMIC database in order to execute. It is divided into three portions: 
1. Pneumonia Data Preproc, which extracts data from MIMIC tables and outputs a patientData table
2. parameterSearch, an accessory program to isolate and observe potential features
3. nextstep, which contains the ML algorithm with which the ICU stay length is predicted. 

All code is original, acknowledgements to Zhipeng Chen for help with debugging. 
