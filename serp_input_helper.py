from re import sub

import pandas as pd
from pandas import ExcelWriter as ew


def load_keywords(inputfile='./keyword_input.xlsx'):
    with open(inputfile,'rt', encoding='utf8') as f:
        excel_file=pd.ExcelFile(inputfile)
        return excel_file.parse(excel_file.sheet_names[0])


def reformat_dataframe(pd_dataframe):
    for date, row in pd_dataframe.T.iteritems():
        row['title'] = remove_extra_text(row['title'])
        #print(row['title'])
    new_col_list = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10']
    return_dataframe = pd_dataframe.reindex(columns=[*pd_dataframe.columns.tolist(), *new_col_list])
    return return_dataframe


def split_dataframe(df, chunk_size=5000):
    listOfDf = list()
    numberChunks = len(df)// chunk_size + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunk_size:(i+1)*chunk_size])
    return listOfDf


def dataframe_to_excel(df,index):
    filename= './temp/excel_input_'+str(index)+'.xlsx'
    if isinstance(df, pd.DataFrame):
        with open(filename, "a+", encoding='utf8') as f:
            writer = ew(filename,  engine='xlsxwriter')
            df.to_excel(writer,'sheet1')
            writer.save()


def remove_extra_text(value):
    return_vaule = value.split("-")[0].strip()
    return_vaule = sub('[,]', '', return_vaule)
    return return_vaule