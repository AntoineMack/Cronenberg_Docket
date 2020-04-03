"""
PIS Reconciliation -
Scripts have 3 main functions
1. Clean raw .txt and csv files
2. Identify existence of client files against a master client list
"""

import pandas as pd, numpy as np
import csv, re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime as dt

################ Afile clean and create dataframe ##########################
print("Hello, make sure you only import CSV UTF-8 file types for files A, B, C and D")

ans = "n"
while ans == "n" or ans != "y":
    try:
        docket = input("What docket are you working on?")
        ans = input("Confirm docket is " + str(docket))
    except:
        print("input not understood")
        continue
    else:
        continue



def Clean_Raw_txt():
    root = tk.Tk()
    root.withdraw()

    a= True
    while a == True:
        try:
            print("Select K Drive PIS .txt file")
            text_file = filedialog.askopenfilename()
            with open (text_file, "r") as myfile:
                raw_Afile = myfile.readlines()
        except:
            a = False
        else:
            break
    Clean_Raw_txt.raw_Afile = raw_Afile

    raw_Afile = [i.replace("\n","") for i in raw_Afile] # remove line breaks
    raw_Afile = [i.replace("_", "") for i in raw_Afile] # remove hyphens
    raw_Afile = [i for i in raw_Afile if "" != i]       # remove empty strings
    raw_Afile = [i for i in raw_Afile if "Received" in i] #filter for PIS
    raw_Afile = [i for i in raw_Afile if "].pdf" in i]    #remove duplicates
    #raw_Afile = [list(dict.fromkeys(raw_Afile))] #remove duplicates w/ dict method
    Clean_Raw_txt.raw_Afile = raw_Afile

if input("Is A file a txt or csv?") == "txt":
    Clean_Raw_txt()
    Afile = pd.DataFrame(Clean_Raw_txt.raw_Afile, columns = ["Received"])
    case_id = pd.Series([], dtype = str)
    Afile["case_id"] = case_id

    def Case_ID_Adder(df, rec_col, dest_col):
        case_pat = re.compile('\d\d\d\d\d\d')
        for i in range(len(df[rec_col])):
            try:
                found = case_pat.search(df[rec_col][i])
                case_id = found.group(0)
                df[dest_col][i] = str(case_id)
            except:
                print(df[rec_col][i] + " does not have a 6 digit case id")
                print("Please check Needles and reconcile value")
                df[rec_col][i] = input("Enter correct 6 digit case id")
                pass
        Case_ID_Adder.df = df

    Case_ID_Adder(Afile, "Received", "case_id")  #A file dataframe READY
    Case_ID_Adder.df.to_csv(str(docket) + " Afile_clean.csv")
    print(str(docket) + " A file is ready! csv created")
else:
    root = tk.Tk()
    root.withdraw()

    a = True
    while a == True:
        try:
            print("Add A file in csv format")
            Afile = filedialog.askopenfilename()
            Afile = pd.read_csv(Afile)
            Afile.rename(columns={"Casenum":"case_id", "Path":"Received"}, \
                                   inplace = True)
            print(str(docket) + " A file is ready! csv created")
        except:
            a = False
        else:
            break
    Clean_Raw_txt.Afile = Afile

#finding and adding case id from file name to case_id column
Afile = Clean_Raw_txt.Afile
Afile["casenum"] = pd.Series([], dtype=str)
for i in range(len(Afile)):
    case_pat = re.compile('\d\d\d\d\d\d')
    try:
        found = case_pat.search(Afile["case_id"][i])
        case_id = found.group(0)
        Afile.at[i,"case_id"] = int(case_id)
    except:
        pass
Afile.to_csv(str(docket) + " Afile_clean.csv")
################ Bfile clean and create dataframe ##########################
root = tk.Tk()
root.withdraw()

a = True
while a == True:
    try:
        print("add case_doc1")
        case_doc1 = filedialog.askopenfilename()
    except:
        a = False
    else:
        break
print("creating df")
case_doc1 = pd.read_csv(case_doc1)  #creating dataframes
Bfile = case_doc1
Bfile.to_csv(str(docket) + ' Bfile_clean.csv')
print(str(docket) + " Bfile ready! csv created")

################ Cfile clean and create dataframe ##########################

# basic pandas filter
print("Select LIT doc file")
lit_file = filedialog.askopenfilename()
lit = pd.read_csv(lit_file)

#
Cfile = lit.loc[(lit["Current_Status"] =="Received From Client") \
| (lit["Current_Status"]=="Received")]

Cfile.to_csv(str(docket) + " Cfile_clean.csv")
print(str(docket) + " Cfile ready! csv created")
################ Dfile clean and create dataframe ##########################
print("Select Portal file")
portal_file = filedialog.askopenfilename()
port = pd.read_csv(portal_file)

port.rename(columns={"Case ID": "case_id"}, inplace = True) #consistency
port[['case_id']].to_csv(str(docket) + " Dfile_clean.csv")
Dfile = port[['case_id']]
print(str(docket) + " Dfile ready! csv created")
################ Master file clean  ########################################
print("Select MASTER docket file")
master_file = filedialog.askopenfilename()
master = pd.read_csv(master_file)

#convert casenum to string and "case_id" for consistency
master.rename(columns = {"casenum":"case_id"}, inplace = True) #rename case_id

master[["case_id","MDL_Client_ID", "class","last_long_name", "first_name"]]\
      .to_csv(str(docket) + " MASTER_clean.csv")
#report = master[["case_id","MDL_Client_ID", "class","last_long_name", "first_name"]]
print(str(docket) + "MASTER file ready! csv created")
#########################Create and Fill master DF for report##################

report = pd.read_csv(str(docket) + " MASTER_clean.csv")
# Afile = pd.read_csv(str(docket) + " Afile_clean.csv")
Bfile = pd.read_csv(str(docket) + " Bfile_clean.csv")
Cfile = pd.read_csv(str(docket) + " Cfile_clean.csv")
Dfile = pd.read_csv(str(docket) + " Dfile_clean.csv")

report["A"] = pd.Series([], dtype=str)
report["B"] = pd.Series([], dtype=str)
report["C"] = pd.Series([], dtype=str)
report["D"] = pd.Series([], dtype=str)


#Adding "X" to column where file exists
count = 0
for i in report['case_id']:
    for a in Afile.case_id:
        if a == int(i):
            print("MATCH")
            indexer = report.loc[report["case_id"]== a, "A"].index[0]
            report.at[int(indexer),"A"] = str("X")
            print(a, "A")
        else:
            pass
    for b in Bfile.case_id:
        if b == int(i):
            indexer = report.loc[report["case_id"]==b, "B"].index[0]
            report.at[int(indexer),"B"] = str("X")
            print(b, "B")
        else:
            pass
    for c in Cfile.case_id:
        if c == int(i):
            indexer = report.loc[report["case_id"]==c, "C"].index[0]
            report.at[int(indexer),"C"] = str("X")
            print(c, "C")
        else:
            pass
    for d in Dfile.case_id:
        if d == int(i):
            indexer = report.loc[report["case_id"]==d, "A"].index[0]
            report.at[int(indexer),"D"] = str("X")
            print(a, "D")
        else:
            pass
    count +=1
    print(count)
now = dt.now()
report.to_csv(str(docket) + " PIS RECON " + now.strftime("%H:%M:%S").\
       replace(":","_")+".csv", index = False)
print(str(docket) + " PIS reconciliation complete")
print("File saved as " + str(docket) + " PIS RECON "+ now.strftime("%H:%M:%S").\
       replace(":","_")+".csv")
