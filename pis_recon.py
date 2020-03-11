"""PIS Reconciliation -
Scripts have 3 main functions
1. Clean raw .txt and csv files
2. Identify existence of client files against a master client list
"""

import pandas as pd, numpy as np
import csv, re
import tkinter as tk
from tkinter import filedialog

################ Afile clean and create dataframe ##########################
print("Hello, make sure the Afile is a .txt file" )
print("Hello, make sure you only import CSV UTF-8 file types for
      files B, C and D")
docket = input("What docket are you working on?")
doc= "y"
    while doc == "y":
        conf = input("Confirm docket is " + str(docket))
        if conf == "y":
            doc = "n"
        elif conf == "n"
            doc = "y"
            continue

text_file = input("Which text file do you want to use for Afile?")

with open (str(text_file), "r") as myfile:
    raw_Afile = myfile.readlines()

raw_Afile = [i.replace("\n","") for i in raw_Afile] # remove line breaks
raw_Afile = [i.replace("_", "") for i in raw_Afile] # remove hyphens
raw_Afile = [i for i in raw_Afile if "" != i]       # remove empty strings

raw_Afile = [i for i in raw_Afile if "Received" in i] #filter for PIS
raw_Afile = [i for i in raw_Afile if "].pdf" in i]    #remove duplicates

raw_Afile = [list(dict.fromkeys(raw_Afile))] #remove duplicates w/ dict method


Afile = pd.DataFrame(raw_Afile, columns = ["Received"])
case_id = pd.Series([], dtype = str)
Afile["case_id"] = case_id


#finding add adding case id from file name to case id row
def Case_ID_Adder(df, rec_col, dest_col):
    case_pat = re.compile('\d\d\d\d\d\d')
    for i in range(len(df[rec_col])):
        try:
            found = case_pat.search(df[rec_col][i])
            case_id = found.group(0)
            df[dest_col][i] = str(case_id)
        except:
            print(df[rec_col][i] + " does not have a 6 digit case id")
            print("Please reconcile values and rerun the script")
            pass

Case_ID_Adder(Afile, "Received", "case_id")  #A file dataframe READY
Afile.to_csv(str(docket) + " Afile_clean.csv")
print(str(docket) + " A file is ready! csv created")

################ Bfile clean and create dataframe ##########################
def Add_Case_docs():
    ans = "y"
    case_doc1 = input("Which file do you want to use for Bfile case_doc1?")
    while ans == "y":
        ans = input("Is there a 2nd case_doc file")
        if ans == "y"
            case_doc2 = input("Which file do you want to use for case_doc2?")
            case_doc1 = pd.read_csv(str(case_doc1))  #creating dataframes
            case_doc2 = pd.read_csv(str(case_doc2),
                        names= list(case_doc1.columns), header = 0)
        elif ans == "n"
            ans = "n"
        elif ans != "y" or "n":
            print('entry no recognized')
            ans = "y"

Add_Case_docs()

b_file_raw = case_doc1.append(case_doc2, ignore_index = True) #appending dfs

Bfile = pd.DataFrame({"case_id":pd.Series([], dtype=str),
                      "file_path":pd.Series([], dtype=str)}, dtype=str)
Bfile_case = []
Bfile_path = []
pis_pat = re.compile('PIS')
for i in range(len(Bfile['file_path'])):

    try:
        found = pis_pat.search(Bfile['file_path'][i])
        pis = found.group(0)
        Bfile_case.append(all_docs['case_id'][i])
        Bfile_path.append(all_docs['file_path'][i])
        print(i)
    except:
        pass

Bfile.to_csv(str(docket) + 'Bfile_clean.csv')
print(str(docket) + " Bfile ready! csv created")

################ Cfile clean and create dataframe ##########################

# basis pandas filter
lit_file = input("which file do you want to use for Cfile LIT doc file")
lit = pd.read_csv(str(lit_file))

#
Cfile = lit[(lit["matcode"] == "EAR") \
    & (lit["Litigation_Document"] == "Plaintiff Information Sheet") \
    & (lit["Current_Status"] == "Received From Client")]

Cfile.to_csv(str(docket) + " Cfile_clean.csv")
print(str(docket) + " Cfile ready! csv created")
################ Dfile clean and create dataframe ##########################

portal_file = input("which file do you want to use for Dfile Portal doc file")
port = pd.read_csv(str(portal_file))

port.rename(columns={"Case ID": "case_id"}, inplace = True) #consistency
port[['case_id']].to_csv(str(docket) + " Dfile_clean.csv")
print(str(docket) + " Dfile ready! csv created")
################ Master file clean  ########################################

master_file = input("which file do you want to use for MASTER docket file")
master = pd.read_csv(master_file)

#convert casenum to string and "case_id" for consistency
master = [str(i) for i in master['casenum']]
master.rename(columns = {"casenum":"case_id"}, inplace = True) #rename case_id

master[["case_id","MDL_Client_ID", "class","last_long_name", "first_name"]]\
      .to_csv(str(docket) + " MASTER_clean.csv")

print(str(docket) + "MASTER file ready! csv created")

#########################Create and Fill master DF for report##################

report = pd.read_csv(str(docket) + " MASTER_clean.csv")
Afile = pd.read_csv(str(docket) + " Afile_clean.csv")
Bfile = pd.read_csv(str(docket) + " Bfile_clean.csv")
Cfile = pd.read_csv(str(docket) + " Cfile_clean.csv")
Dfile = pd.read_csv(str(docket) + " Dfile_clean.csv")

report["A"] = pd.Series([],dtype=str)
report["B"] = pd.Series([],dtype=str)
report["C"] = pd.Series([],dtype=str)
report["D"] = pd.Series([],dtype=str)

#Adding "X" to column where file exists
for i in range(len(report['case_id'])):
    if any(Afile.case_id.isin([report['case_id'][i]])): #search Afile
        report['A'][i] = "X"
    else:
        pass
    if any(Bfile.case_id.isin([report['case_id'][i]])): #search Bfile
        report['B'][i] = "X"
    else:
        pass
    if any(Cfile.case_id.isin([report['case_id'][i]])): #search Cfile
        report['C'][i] = "X"
    else:
        pass
    if any(Dfile.case_id.isin([report['case_id'][i]])): #search Dfile
        report['D'][i] = "X"
    else:
        pass
