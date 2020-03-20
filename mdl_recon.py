'''
MDL recon agains JLG submission summary.
'''
#Search filename for values
#send values to designated columns
#Search for each specific document type name.  sheeeesh!!!

#Search filename for values
#send values to designated columns
#Search for each specific document type name.  sheeeesh!!!

def File_Name_Parser(df, filename_col):
    mdlc_pat = re.compile('\d{5,}_')   #mdl id regex
    docid_pat = re.compile('_\d\d_')   #doc id regex

    dd_onefive = re.compile("Form DD 2215")  #doctype regex
    dd_onesix = re.compile("Form DD 2216")
    va_twoone = re.compile("VA Form 21-4138")
    va_onezero = re.compile("VA Form 10-2364")
    vba_work = re.compile("VBA Worksheet 1305")
    rat_dec = re.compile("Rating Decision")
    dd_onefour = re.compile("Form DD 214")
    va_a = re.compile("VA Form 10-2364a")
    va_ez = re.compile("VA Form 21-526 EZ")
    va_ninetwo = re.compile("VA Form 21-4192")
    va_fourzero = re.compile("VA Form 21-8940")
    other = re.compile("Other")
    dd_ttonefour = re.compile("Form DD 2214")

    caseid_pat = re.compile('_\d{6}\.')  # case id regex


    form_list = [dd_onefive, dd_onesix, va_twoone, va_onezero,
           vba_work, rat_dec, dd_onefour, va_a, va_ez, va_ninetwo,
           va_fourzero, other, dd_ttonefour]

    for i in range(len(df[filename_col])):
        try:
            found = mdlc_pat.search(df[filename_col][i])
            value = found.group(0)
            df["MDLC_ID"][i] = str(value)            #MDL ID
        except:
            pass
        try:
            found = docid_pat.search(df[filename_col][i])
            value = found.group(0)
            df["DocID"][i] = str(value)              #DOC ID
        except:
            pass
        for f in form_list:
            try:
                found = f.search(df[filename_col][i])
                value = found.group(0)
                df["Document Type"][i] = str(value) #Document type
            except:
                pass
        try:
            found = caseid_pat.search(df[filename_col][i])
            value = found.group(0)
            value = str(value).replace(".","")
            df["case_id"][i] = str(value)          #Case ID
        except:
            pass


            """Ask to reconcile 5 digit case ids"""

"""populating MDL RECON


for i in reg_test.Plaintiff_ID:
    index_count = 0
    indexer1 = reg_test.loc[reg["Plaintiff_ID"] == i, "Plaintiff_Name"].index[0]
    name = reg_test.loc[reg["Plaintiff_ID"] == i, "Plaintiff_Name"].get(indexer1)
    print(name)
    for j in jlg.loc[jlg["MDLC_ID"]==i, "Document_Type"]:   #JLG to MDL search
        jlg_pat = re.compile(j)
        count = 0
        for k in mdl.loc[mdl["MDLC_ID"] == i, "Document_Type"]:
            count +=1
            final = len(mdl.loc[mdl["MDLC_ID"] == i, "Document_Type"])
            try:
                found = jlg_pat.search(k)
                value = found.group(0)                #JGL = MDL
                doc_type = j                          #Setting value of Document Type
                if j == "Form DD 2214":
                    docid = "1"
                elif j == "Form DD 2215":             #Setting value of DocID
                    docid = "2"
                elif j == "Form DD 2216":
                    docid = "3"
                elif j == "Audiogram_Other Test":
                    docid = "4"
                elif j == "Disability Record":        #FOUND DOC IN JLG AND MDL
                    docid = "5"
                elif j == "VBA Worksheet 1305":
                    docid = "9"
                elif j == "Rating Decision":
                    docid = "16"
                elif j == "Form DD 214":
                    docid = "19"
                elif j == "VA Form 10-2364a":
                    docid = "15"
                elif j == "VA Form 21-526 EZ":
                    docid = "13"
                else:
                    docid = "18"

                #mdl.loc[(mdl["MDLC_ID"] == "19183") & (mdl["Document_Type"] == "Form DD 2215"), "Document ID"]
                date_index1 = mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Date_Uploaded"].index[0]
                date_upload1 = mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Date_Uploaded"].get(date_index1)  #setting value of Date_Uploaded

                mdl_index1 =  mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Document ID"].index[0]
                mdl_doc_id1 = mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Document ID"].get(mdl_index1)
                jlg_status = "X"                      #Set In_JLG
                mdl_status = "X"                      #Set In_JLG

#                 if rec_mdl.iloc[count-1,3] == mdl_doc_id1:      #TRYING TO FIX DOCUMENT ID'S
#                     mdl_doc_id1 = int(mdl_doc_id1) +1
#                 else:
#                     pass

                new_row = pd.DataFrame([[i, name, doc_type, mdl_doc_id1 , date_upload1, docid,
                                         jlg_status, mdl_status]], columns = list(rec_mdl.columns))
                rec_mdl = rec_mdl.append(new_row)
                print("MDL/ JLG row made")
                index_count +=1
                break                                   #end cylce, search for new j in k
            except:
                if count == final:
                    doc_type = j                                #if the JLG document is NOT found in the MDL list.
                    if j == "Form DD 2214":
                        docid = "1"
                    elif j == "Form DD 2215":                   #DocID
                        docid = "2"
                    elif j == "Form DD 2216":
                        docid = "3"
                    elif j == "Audiogram_Other Test":           #IN JLG, NOT IN MDL
                        docid = "4"
                    elif j == "Disability Record":
                        docid = "5"
                    elif j == "VBA Worksheet 1305":
                        docid = "9"
                    elif j == "Rating Decision":
                        docid = "16"
                    elif j == "Form DD 214":
                        docid = "19"
                    elif j == "VA Form 10-2364a":
                        docid = "15"
                    elif j == "VA Form 21-526 EZ":
                        docid = "13"
                    else:
                        docid = "18"
                                                              #no mdl_doc_id, or upload date
                    jlg_status = "X"
                    mdl_status = ""
                    in_jlg_row = pd.DataFrame([[i, name, doc_type, "","", "",
                                                jlg_status, mdl_status]], columns = list(rec_mdl.columns))
                    rec_mdl = rec_mdl.append(in_jlg_row)
                    print("JLG row made")
                    index_count  +=1
                    count = 0
                else:
                    pass

    for k in mdl.loc[mdl["MDLC_ID"] == i, "Document_Type"]:   # MDL to JLG search
        mdl_pat = re.compile(k)
        count = 0
        for j in jlg.loc[jlg["MDLC_ID"]==i, "Document_Type"]:
            count +=1
            final = len(jlg.loc[jlg["MDLC_ID"]==i, "Document_Type"])
            try:
                found = mdl_pat.search(j)
                value = found.group(0)
                break                                   #end cylce, search for new k in j
            except:
                if count == final:
                    doc_type = k    #doc_type was k                          #Setting value of Document Type
                    if k == "Form DD 2214":
                        docid2 = "1"
                    elif k == "Form DD 2215":                 #Setting value of DocID
                        docid2 = "2"
                    elif k == "Form DD 2216":
                        docid2 = "3"
                    elif k == "Audiogram_Other Test":
                        docid2 = "4"
                    elif k == "Disability Record":           #IN MDL NOT IN JLG
                        docid2 = "5"
                    elif k == "VBA Worksheet 1305":
                        docid2 = "9"
                    elif k == "Rating Decision":
                        docid2 = "16"
                    elif k == "Form DD 214":
                        docid2 = "19"
                    elif k == "VA Form 10-2364a":
                        docid2 = "15"
                    elif k == "VA Form 21-526 EZ":
                        docid2 = "13"
                    else:
                        docid2 = "18"
                        pass
                    docid2 = docid2
                    date_index2 = mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Date_Uploaded"].index[0]
                    date_upload2 = mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Date_Uploaded"].get(date_index2)  #setting value of Date_Uploade

                    mdl_index2 = mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Document ID"].index[0]
                    mdl_doc_id2 = mdl.loc[(mdl["MDLC_ID"] == i) & (mdl["Document_Type"] == doc_type), "Document ID"].get(mdl_index2)

                    jlg_status = ""                      #Set In_JLG
                    mdl_status = "X"                      #Set In_JLG

#                     if rec_mdl.iloc[count,3] == mdl_doc_id2:
#                         mdl_doc_id2 = str(int(mdl_doc_id2) +1)
#                     else:
#                         pass
                    in_mdl_row = pd.DataFrame([[i,name, doc_type,mdl_doc_id2,date_upload2, docid2 ,jlg_status, mdl_status]],
                                                columns = list(rec_mdl.columns))
                    rec_mdl = rec_mdl.append(in_mdl_row)
                    print("MDL row made")
                    print(count, final)
                    index_count +=1
                    count = 0
                else:
                    pass
