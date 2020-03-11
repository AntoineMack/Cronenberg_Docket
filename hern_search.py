"""Initial Search Program for hernia mesh docket. Looking to accomplish
4 functions.
    1.) Spell check medical terms,
    2.) User input keyword search (exact and like)
    3.) Artifact search and quantity, ie "*" for 2x
    4.) Range search of 2 words within x # of words

    """
import pandas as pd, numpy as np
import re
import csv

#load csv
user_excel = input('insert path of file')
doc = pd.read_csv(user_excel)

#set terms to search from user
class TermsList:
    terms = []
    more = 'y'
    while more == 'y':
        new_term = input('insert term to search')
        terms.append(new_term)
        more = input('add another word? y or n')
        if more.lower() == 'y':
            more = 'y'
            continue
        elif more.lower() == "n":
            more = 'n'

#set artifacts to search and how many from user
class Artifacts:
    af = []
    more = 'y'
    while more == 'y':
        new_art = input('insert artifact to search')
        af.append(new_art)
        more = input('add another artifact? y or n')
        if more.lower() == 'y':
            more = 'y'
            continue
        elif more.lower() == "n":
            more = 'n'

#set 2 term range & proximity
class Proximity:
    group1 = []
    more = 'y'
    while more == 'y'
    fstword = input('insert 1st word')
    sndword = input('insert 2nd word')
    group1.extend((fstword,sndword))
    prox = input('insert # of words apart')

#locate text column.  User must for insure text is 3rd column
rel = str(doc.columns[2])
for i in range(len(doc)):
    if any(re.search(TermsList.terms, i))
        doc.loc[i, rel] = "X"


#file to csv
save_name = str(input('Enter file name to save:'))
doc.to_csv(save_name)

)
