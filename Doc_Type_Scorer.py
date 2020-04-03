"""
Add page numbers to sequential mail for easy sorting
"""
import pandas as pd, numpy as np
import re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime as dt
#############################################################################

root = tk.Tk()
root.withdraw()

a = True
while a == True:
    try:
        print("Add Mail File")
        ml = filedialog.askopenfilename()
        ml = pd.read_csv(ml)
    except:
        a = False
    else:
        break

def Force_Int(df,case_col,name_col):
    mail_pat = re.compile('\d{5,}')
    try:
        for i in range(len(df[case_col])):
            print(df[case_col][i])
            found = mail_pat.search(df[case_col][i])
            print(found)
            casenum = found.group(0)
            df.at[i, case_col] = int(casenum)
    except:
        for i in range(len(df[case_col])):
            print(df[name_col][i])
            found = mail_pat.search(df[name_col][i])
            print(found)
            casenum = found.group(0)
            df.at[i, case_col] = int(casenum)
    Force_Int.ml = ml


def Int_Adder(df, case_col, page_col):
    list_counter = 1
    for i in range(len(df[case_col])):
        if i == len(df[case_col])-1:
            df.at[i, page_col] = int(list_counter)
        elif df[case_col][i] == df[case_col][i +1]:
            df.at[i, page_col] = int(list_counter)
            list_counter +=1
        elif df[case_col][i] != df[case_col][i +1]:
            df.at[i, page_col] = int(list_counter)
            list_counter =1
        else:
            pass


Force_Int(ml, "Casenum", "Name")
Int_Adder(Force_Int.ml, "Casenum", "Pg Num")

#ml["Pg Num"] = [int(i) for i in ml["Pg Num"]]

print("Page numbers added")
now = dt.now()
ml.to_csv("Doc_Type_Pg_Num" + now.strftime("%H:%M:%S").replace(":","_")+".csv")
