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

################ Afile clean and create dataframe ##########################
print("Hello, make sure the Afile is a .txt file" )
print("Hello, make sure you only import CSV UTF-8 file types for files B, C and D")

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

Clean_Raw_txt()
Afile = pd.DataFrame(Clean_Raw_txt.raw_Afile, columns = ["Received"])
case_id = pd.Series([], dtype = str)
Afile["case_id"] = case_id

#finding and adding case id from file name to case_id column
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
#remove duplicate names here!!!
#print report of how many duplicates removed
Case_ID_Adder.df.to_csv(str(docket) + " Afile_clean.csv")
print(str(docket) + " A file is ready! csv created")

################ Bfile clean and create dataframe ##########################
def Add_Case_docs():
    root = tk.Tk()
    root.withdraw()

    a = True
    while a == True:
        try:
            print("add case_doc1")
            case_doc1 = filedialog.askopenfilename()
            print("add case_doc2")
            case_doc2 = filedialog.askopenfilename()
        except:
            a = False
        else:
            break
    print("creating df")
    case_doc1 = pd.read_csv(case_doc1)  #creating dataframes
    case_doc2 = pd.read_csv(case_doc2 ,names= list(case_doc1.columns), header = 0)
    Add_Case_docs.case_doc1 = case_doc1
    Add_Case_docs.case_doc2 = case_doc2

Add_Case_docs()

b_file_raw = Add_Case_docs.case_doc1.append(Add_Case_docs.case_doc2, ignore_index = True) #appending dfs
b_file_raw.drop(columns= ['matcode', 'document_id', 'category',
       'original_file_size', 'Staff_Created', 'Date_Added', 'date_created'], inplace = True)

Bfile = pd.DataFrame({"case_id":pd.Series([], dtype=str),
                      "file_path":pd.Series([], dtype=str)}, dtype=str)
Bfile_case = []
Bfile_path = []
pis_pat = re.compile('PIS')
for i in range(len(b_file_raw['file_path'])):

    try:
        found = pis_pat.search(b_file_raw['file_path'][i])
        pis = found.group(0)
        Bfile_case.append(b_file_raw['case_id'][i])
        Bfile_path.append(b_file_raw['file_path'][i])
        print(i)
    except:
        pass

Bfile["case_id"] = Bfile_case
Bfile["file_path"] = Bfile_path

Bfile.to_csv(str(docket) + ' Bfile_clean.csv')
print(str(docket) + " Bfile ready! csv created")

################ Cfile clean and create dataframe ##########################

# basic pandas filter
print("Select LIT doc file")
lit_file = filedialog.askopenfilename()
lit = pd.read_csv(lit_file)

#
Cfile = lit[(lit["matcode"] == "EAR") \
    & (lit["Litigation_Document"] == "Plaintiff Information Sheet") \
    & (lit["Current_Status"] == "Received From Client")]

Cfile.to_csv(str(docket) + " Cfile_clean.csv")
print(str(docket) + " Cfile ready! csv created")
################ Dfile clean and create dataframe ##########################
print("Select Portal file")
portal_file = filedialog.askopenfilename()
port = pd.read_csv(portal_file)

port.rename(columns={"Case ID": "case_id"}, inplace = True) #consistency
port[['case_id']].to_csv(str(docket) + " Dfile_clean.csv")
print(str(docket) + " Dfile ready! csv created")
################ Master file clean  ########################################
print("Select MASTER docket file")
master_file = filedialog.askopenfilename()
master = pd.read_csv(master_file)

#convert casenum to string and "case_id" for consistency
[str(i) for i in master['casenum']]
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
    print(i)
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

report.to_csv(str(docket) + " PIS RECON COMPLETE.csv")
print(str(docket) + " PIS reconciliation complete")
print("File saved as " + str(docket) + " PIS RECON COMPLETE.csv")
