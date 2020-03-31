import pandas as pd
import re, csv
import tkinter as tk
from tkinter import filedialog
from datetime import datetime as dt
'''
Rename to MDL file counts
Takes in MDL Doc Submission Report and reports a count of documents in
6 categories PIS, Complaint, Touhy Request, Touhy Response, MR, Other
'''

### import MDL Submission Report
root = tk.Tk()
root.withdraw()
a = True
while a == True:
    try:
        print("Add MDL submission report file")
        mdl = filedialog.askopenfilename()
        print("JLG MDL submission report added")
    except:
        a = False
    else:
        break
mdl = pd.read_csv(mdl)

### import MASTER
root = tk.Tk()
root.withdraw()
a = True
while a == True:
    try:
        print("Add MDL_ID/ Casenum Master file")
        master = filedialog.askopenfilename()
        print("MDL_ID/ Casenum Master added")
    except:
        a = False
    else:
        break
master = pd.read_csv(master)

#rename columns
mdl.rename(columns = {"MDLC ID":"MDLC_ID", "Plaintiff Name":"Plaintiff_Name",
                     "Document Type":"Document_Type"}, inplace = True)
master.rename(columns={"MDL ID":"MDLC_ID"}, inplace = True)

#make df of unique MDLC_ID
mdl2= pd.DataFrame([],dtype=str)
mdl2["MDLC_ID"] = pd.Series(master.MDLC_ID, dtype=str)
mdl2["Plaintiff_Name"] = pd.Series([], dtype=str)
mdl2["casenum"] = pd.Series([], dtype=str)
mdl2["PIS"] = pd.Series([], dtype=str)
mdl2["Complaint"] = pd.Series([], dtype=str)
mdl2["Touhy_Request"] = pd.Series([], dtype=str)
mdl2["Touhy_Response"] = pd.Series([], dtype=str)
mdl2["MR"] = pd.Series([], dtype=str)
mdl2["Other"] = pd.Series([], dtype=str)

### make sure all columns are strings and fill nulls

master["MDLC_ID"].fillna(" ",inplace = True)
master["MDLC_ID"] = [str(i)  for i in master["MDLC_ID"]]
master["casenum"] = [str(i) for i in master["casenum"]]
mdl["MDLC_ID"] = [str(i) for i in mdl["MDLC_ID"]]

### add Master Plaintiff name
for i in list(master["MDLC_ID"]):
    first_name = list(master.loc[master["MDLC_ID"]==i, "first_name"])[0]
    last_name = list(master.loc[master["MDLC_ID"]==i, "last_long_name"])[0]
    print(str(last_name) + ", " + str(last_name))
    Plaintiff = str(last_name) + ", " + str(first_name)
    mdl2.loc[mdl2["MDLC_ID"]==i,"Plaintiff_Name"] = Plaintiff
#adding casenum
for i in list(mdl2["MDLC_ID"]):
    print(i)
    try:
        number = master.loc[master["MDLC_ID"] == i, 'casenum']
        mdl2.loc[mdl2["MDLC_ID"] == i, 'casenum'] = number
    except:
        pass

# add names to mdl id's
# index = 0
# for i in list(mdl2["MDLC_ID"]):
#     print(i)
#     name_list = list(master.loc[master['MDLC_ID'] == i, "Plaintiff_Name"])
#     name = name_list[0]
#     mdl2["Plaintiff_Name"][index] = name
#     index+=1
#     print(name)

### Begin counts & setting document catagories
print("Counting Client Documents")
report = mdl
PIS = ["Unfiled Case Census Form"]
Comp = ["Unfiled Case Short Form Complaint","File Stamped Short Form Complaint"]
Tou =["VA Touhy Request", "Touhy Request"]
Res = ["Touhy Response - Enlisted Record Brief","Touhy Response - Form DD 214",
"Touhy Response - NCOER","Touhy Response - RCMS ARB","Touhy Response - PQR",
"Touhy Response - NGB Form 22","Touhy Response - Form DD 215","Touhy Response - OER"]
MR = ["Medical Records", "Form DD 2215","Form DD 2216","Disability Records",
"Rating Decision","Audiogram or Other Hearing Test outside the military",
"Form DD 214","VA Form 21-4138","VA Form 10-2364","Other","VBA Worksheet 1305",
"VA Form 10-2354a","VA Form 21-256 EZ","VA Form 21-4192","VA Form 21-8940"]
Other = ["Bellwether Selection Sheet",
"Verification of Census Form - Signature for 3.9.2020 amended Census Questionnaire",
"Request for Dismissal from Administrative Docket","Notice of Representation Issue",
"Verification of Census Form"]


def Counter(mdl2, report):
    for i in mdl2["MDLC_ID"]:
        print(type(i))
        doc_list = list(report.loc[report["MDLC_ID"]== i, "Document_Type"])
        print(i,doc_list)
        unique_doc = set(doc_list)
        PIS_count = 0
        Comp_count = 0
        Tou_count = 0
        Res_count = 0
        MR_count = 0
        Other_count = 0
        for j in unique_doc:
            try:
                if j in PIS:
                    PIS_count += doc_list.count(j)
            except:
                pass
            try:
                if j in Comp:
                    Comp_count += doc_list.count(j)
            except:
                pass
            try:
                if j in Tou:
                    Tou_count += doc_list.count(j)
            except:
                pass
            try:
                if j in Res:
                    Res_count += doc_list.count(j)
            except:
                pass
            try:
                if j in MR:
                    MR_count += doc_list.count(j)
            except:
                pass
            try:
                if j in Other:
                    Other_count += doc_list.count(j)
            except:
                pass
        mdl2.loc[mdl2["MDLC_ID"]==i, "PIS"] = PIS_count
        mdl2.loc[mdl2["MDLC_ID"]==i, "Complaint"] = Comp_count
        mdl2.loc[mdl2["MDLC_ID"]==i, "Touhy_Request"] = Tou_count
        mdl2.loc[mdl2["MDLC_ID"]==i, "Touhy_Response"] = Res_count
        mdl2.loc[mdl2["MDLC_ID"]==i, "MR"] = MR_count
        mdl2.loc[mdl2["MDLC_ID"]==i, "Other"] = Other_count


Counter(mdl2,report)
now = dt.now()
mdl2.to_csv("Doc_Counts_MDL_Report" + now.strftime("%H_%M_%S")+ ".csv")
print("Doc_Counts_MDL_Report" + now.strftime("%H_%M_%S")+ ".csv", " is saved")
