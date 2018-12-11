import pandas as pd
from pandas import DataFrame, Series
import numpy as np


# Set ipython's max row display
#pd.set_option('display.max_row', 1000)

# Set iPython's max column width to 50
# pd.set_option('display.max_columns', 10)

# Read file
# df = pd.read_excel('NATIONAL_Summary_08.xls', sheet_name = 'all', skiprows=3, header=[0,1], index_col = [0, 1], na_values = '*', skipfooter = 5)

# Washington 2013
wa_2013 = pd.read_excel('../data/Washington_Summary_13.xls', sheet_name = 'All', skiprows=4, header=[0,1], 
        index_col = [0,1], usecols = 'B:AL', na_values = {'*',''}, skipfooter = 5)
clean_indexes(wa_2013)
wa_2013 = clean_data(wa_2013)

wa_2013.loc[('MEAN SCORE','')]

wa_2013.rename(index={('MEAN SCORE', ''):('MEAN GRADE', 'MG')}, inplace=False)

wa_2013[('NUMBER OF STUDENTS FOR EACH EXAMINATION','TOTAL EXAMS')]

wa_2013.rename(index={6:'MG'})

# move mean score to second level of index
wa_2013.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2013.index])

# remove TOTAL
wa_2013.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2013.index])

# add first level of index to blanks
def correct_levels(indx):
    first_level_name = ''
    new_indx = []

    for i in wa_2013.index:
        if len(i[0]) > 0:
            first_level_name = i[0]
        new_indx.append((i[0], i[1]))

    return(new_indx)

        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2013.index]

# Washington_Summary_12.xls    washington-summary-2015.xlsx
# NATIONAL_Summary_09.xls      WASHINGTON_Summary_08.xls    Washington_Summary_13.xls    washington-summary-2016.xlsx
# NATIONAL_Summary_10.xls      WASHINGTON_Summary_09.xls    national-summary-2015.xlsx   washington-summary-2017.xlsx
# NATIONAL_Summary_11.xls      WASHINGTON_Summary_10.xls    national-summary-2016.xlsx   washington-summary-2018.xlsx
# National-Summary-2014.xlsx   WASHINGTON_Summary_11.xls    national-summary-2017.xlsx
# National_Summary_12.xls      Washington-Summary-2014.xlsx national-summary-2018.xlsx





# Change AP Grade index for Mean Grade to MG
df.loc[('MEAN GRADE',),]

df.rename(index={('MEAN GRADE', 'T'): ('MEAN GRADE', 'MG')}, inplace=False)

df.rename(index={'MEAN GRADE': 'MG'}, inplace=False)

df.rename(index={6:'MG'})

# Remove \n from column names
def clean_indexes(df=df):

    # Clean Column Names
    col_0 = [i[0] for i in df.columns]
    col_1 = [i[1] for i in df.columns]
    column_names = col_0 + col_1
    column_names = list(set(column_names))
    
    for i in column_names:
        if type(i) is str:
            df.rename(columns={i: i.replace('\n', ' ')}, inplace=True)

    for i in column_names:
        if type(i) is str:
            df.rename(columns={i: i.strip()}, inplace=True)

    # Clean indexes
    index_0 = [i[0] for i in df.index]
    index_1 = [i[1] for i in df.index]
    index_names = index_0 + index_1
    index_names = list(set(index_names))

    for i in index_names:
        if type(i) is str:
            df.rename(index={i: i.replace('\n', ' ')}, inplace=True)

    for i in index_names:
        if type(i) is str:
            df.rename(index={i: i.strip()}, inplace=True)

    # name indexes
    df.index.rename('Ethnicity', level=0, inplace = True)
    df.index.rename('AP Score', level=1, inplace = True)
    
    # remove column name
    df.columns.rename('', level=0, inplace = True)

def clean_data(df=df):

    # remove spaces 
    df = df.applymap(lambda x: x.strip() if type(x) is str else x) 

    # remove asterisks
    df = df.applymap(lambda x: np.nan if type(x) is str and ('*' in x)  else x) 

    # remove empty strings
    df = df.applymap(lambda x: np.nan if type(x) is str and (x == '' )  else x) 
    
    return(df)




