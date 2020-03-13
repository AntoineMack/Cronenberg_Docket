import tkinter as tk, pandas as pd
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
#
# while True:
#     try:
#         file_path = filedialog.askopenfilename()
#         df = pd.read_csv(file_path)
#     except:
#         print("File type incorrect")
#     else:
#         break
#
# print("df is set")
a= True
while a == True:
    try:
        text_file = filedialog.askopenfilename()
        with open (str(text_file), "r") as myfile:
            raw_Afile = myfile.readlines()
    except:
        a = False
    else:
        break
