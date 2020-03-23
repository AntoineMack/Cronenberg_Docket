import pandas as pd
import re, csv
import tkinter as tk
from tkinter import filedialog

"""
The MDL Reconciler takes in 3 files
1.) JLG submissions to the MDL
2.) MDL submission Report
3.) MDL Plaintiff Registration

Output:  Reconciler will output csv with mdlc_id, Plaintiff name,
Document Type, 2 columns indicating the # of a given document types
in the JLG submission and MDL submission.  Last column is called
"Issue", it marks an "X" to JLG submitted files that are not equal
to MDL reported files.
"""


### Import JLG submission
root = tk.Tk()
root.withdraw()

a = True
while a == True:
    try:
        print("Add JLG submission file")
        jlg = filedialog.askopenfilename()
        print("JLG submission added")
    except:
        a = False
    else:
        break

# jlg = pd.read_csv("JLG Submitted.csv") ***for local use
#add new columns to jlg sub
jlg = pd.read_csv(jlg)
mdlc_id = pd.Series([], dtype= str)
docid = pd.Series([], dtype= str)
doctype = pd.Series([], dtype= str)
plaint = pd.Series([], dtype= str)
caseid = pd.Series([], dtype= str)
jlg["MDLC_ID"] = mdlc_id
jlg["DocID"] = docid
jlg["Document Type"] = doctype
jlg["case_id"] = caseid


def File_Name_Parser(df, filename_col):
    mdlc_pat = re.compile('\d{5,}_')   #mdl id regex
    docid_pat = re.compile('_\d\d_')   #doc id regex

    dd_onefive = re.compile("Form DD 2215")  #doctype regex
    dd_onesix = re.compile("Form DD 2216")
    va_twoone = re.compile("VA Form 21-4138")
    va_onezero = re.compile("VA Form 10-2364")
    audiogram = re.compile("Audiogram_Other Test")
    dis_rec = re.compile("Disability Record")
    vba_work = re.compile("VBA Worksheet 1305")
    rat_dec = re.compile("Rating Decision")
    dd_onefour = re.compile("Form DD 214")
    va_a = re.compile("VA Form 10-2364a")
    va_ez = re.compile("VA Form 21-526 EZ")
    va_ninetwo = re.compile("VA Form 21-4192")
    va_fourzero = re.compile("VA Form 21-8940")
    other = re.compile("Other")
    dd_ttonefour = re.compile("Form DD 2214")

    caseid_pat = re.compile("_\d{6}") # case id regex


    form_list = [dd_onefive, dd_onesix, va_twoone, va_onezero, audiogram,
           dis_rec, vba_work, rat_dec, dd_onefour, va_a, va_ez, va_ninetwo,
           va_fourzero, other, dd_ttonefour]

    for i in range(len(df[filename_col])):
        try:
            found = mdlc_pat.search(df[filename_col][i])
            value = found.group(0)
            value = str(value).replace("_","")
            df["MDLC_ID"][i] = str(value)            #MDL ID, drop back underscore
        except:
            pass
        try:
            found = docid_pat.search(df[filename_col][i])
            value = found.group(0)
            value = str(value).replace("_","")
            df["DocID"][i] = str(value)              #DOC ID
        except:
            pass
        for f in form_list:
            try:
                found = f.search(df[filename_col][i])
                value = found.group(0)
                df["Document Type"][i] = str(value) #Document type
                break
            except:
                df["Document Type"][i] = str("OTHER")
                pass
        try:
            found = caseid_pat.search(df[filename_col][i])
            value = found.group(0)
            value = str(value).replace("_","")
            df["case_id"][i] = str(value)          #Case ID
        except:
            pass

File_Name_Parser(jlg, "Filename")

### Add 5 digit case_id reconciler. ie if len(case_id) != 6
jlg.case_id.iloc[49]= '334456'
jlg.loc[jlg["case_id"]=="309384"]

# Import MDL submission
root = tk.Tk()
root.withdraw()
a = True
while a == True:
    try:
        print("Add MDL submission file")
        mdl = filedialog.askopenfilename()
        print("MDL submission added")
    except:
        a = False
    else:
        break
mdl = pd.read_csv(mdl)

# Import MDL Plaintiff Registration
root = tk.Tk()
root.withdraw()
a = True
while a == True:
    try:
        print("Add MDL Plaintiff Registration file")
        reg = filedialog.askopenfilename()
        print("MDL Plaintiff Registration added")
    except:
        a = False
    else:
        break
reg = pd.read_csv(reg)
#mdl = pd.read_csv("MDL Sub Submission Summary Report_2885_lf (3).csv") ***for local use
#reg = pd.read_csv("MDL Plaintiff Registration Submission Status Report_2885_lf (4).csv") ***for local use

#Changing names of columns for continuity
replace_dic = {"Audiogram or Other Hearing Test outside the military":"Audiogram_Other Test",
               "Disability Records":"Disability Record", "VA Form 10-2354a":"VA Form 10-2364a",
               "Other":"OTHER"}
mdl.replace(replace_dic, inplace=True)
jlg.rename(columns={"Document Type":"Document_Type"}, inplace = True)
mdl.rename(columns={"MDLC ID":"MDLC_ID",'Plaintiff Name':'Plaintiff_Name',
                    'Law Firm':'Law_Firm','Filed Case Plaintiff':'Filed_Case_Plaintiff',
                    'Document Type':'Document_Type', "Date Uploaded":"Date_Uploaded"}, inplace = True)

#convert JLG id to strings
jlg["MDLC_ID"] = [int(i) for i in jlg["MDLC_ID"]]
# reducing reg to relevant columns
reg = reg[["Plaintiff_Name", "Plaintiff_ID"]]
#reg_test = reg.head(100) ***for testing and local use
#build new_rec_mdl DataFrame
column_list = ['MDLC_ID', 'Plaintiff_Name','Document_Type',
       '#_doc_in_JLG', '#_docs_in_MDL','Issue']
new_rec_mdl = pd.DataFrame([["","","","","",""]],columns=column_list)

#creating NEW RECON MDL
for i in reg.Plaintiff_ID:
    name_index = reg.loc[reg["Plaintiff_ID"] == i, "Plaintiff_Name"].index[0]
    name = reg.loc[reg["Plaintiff_ID"] == i, "Plaintiff_Name"].get(name_index)
    print(name)
    index_flag = 0
    used_docs = []
    issue = ""
    for j in jlg.loc[jlg["MDLC_ID"]==i, "Document_Type"]:
        print(j)
        try:
            indexer = jlg.loc[jlg['MDLC_ID']==i, "Document_Type"].index[index_flag]
            found_doc = jlg.loc[jlg['MDLC_ID']==i, "Document_Type"].get(indexer)
            num_of_docs_jlg = len(jlg.loc[(jlg["MDLC_ID"]==i) & (jlg["Document_Type"]== str(found_doc))])
            index_flag += 1
            used_docs.append(found_doc)
            num_of_docs_mdl = len(mdl.loc[(mdl["MDLC_ID"]==i) & (mdl["Document_Type"]== str(found_doc))])
            if num_of_docs_jlg != num_of_docs_mdl:
                issue = "X"
            else:
                issue = ""
                pass
            new_row = pd.DataFrame([[i, name, found_doc, num_of_docs_jlg,num_of_docs_mdl, issue]], columns = list(new_rec_mdl.columns))
            new_rec_mdl = new_rec_mdl.append(new_row)
            new_rec_mdl.drop_duplicates(keep="first", inplace=True)
                         #### Add statement to remove duplicates after every row add
            print("new row added")
        except:
            pass
    issue = ""
    mdl_index_flag = 0
    num_of_docs_jlg = 0
    for k in mdl.loc[mdl["MDLC_ID"]== i, "Document_Type"]:
        issue = ""
        print("USED DOCS: ",used_docs)
        if k not in used_docs:
            try:
                print(k, "mdl search")
                indexer2 = mdl.loc[mdl["MDLC_ID"]==i, "Document_Type"].index[mdl_index_flag]
                mdl_index_flag += 1
                mdl_found_doc = mdl.loc[mdl["MDLC_ID"]==i, "Document_Type"].get(indexer2)
                print(mdl_found_doc)
                num_of_docs_mdl = len(mdl.loc[(mdl["MDLC_ID"]==i) & (mdl["Document_Type"]== str(mdl_found_doc))])
                print(num_of_docs_mdl)

                new_row2 = pd.DataFrame([[i, name, mdl_found_doc, str(num_of_docs_jlg), str(num_of_docs_mdl),
                                          issue]], columns = list(new_rec_mdl.columns))
                new_rec_mdl = new_rec_mdl.append(new_row2)
                new_rec_mdl.drop_duplicates(keep="first", inplace=True)

                print("new MDL row added")
                          #### Add statement to remove duplicates after every row add
            except:
                pass

new_rec_mdl.drop_duplicates(subset= ["MDLC_ID", "Document_Type"], keep= "first", inplace = True)

new_rec_mdl.to_csv("new_rec_mdl.csv")
