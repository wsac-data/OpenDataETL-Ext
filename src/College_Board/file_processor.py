import pandas as pd
from pandas import DataFrame, Series
import numpy as np

# This file was developed using a REPL process in ipython

# Set ipython's max row display
pd.set_option('display.max_row', 500)

# Set iPython's max column width to 50
# pd.set_option('display.max_columns', 10)


# clean up column names and row names
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
    # df.index.rename('Ethnicity', level=0, inplace = True)
    # df.index.rename('AP Score', level=1, inplace = True)
    
    # remove column name
    # df.columns.rename('', level=0, inplace = True)

    df.rename_axis(['number','subject'],axis = 1, inplace=True)

# clean up data
def clean_data(df=df):

    # remove spaces 
    df = df.applymap(lambda x: x.strip() if type(x) is str else x) 

    # remove asterisks
    df = df.applymap(lambda x: np.nan if type(x) is str and ('*' in x)  else x) 

    # remove empty strings
    df = df.applymap(lambda x: np.nan if type(x) is str and (x == '' )  else x) 

    # remove totals prior to reshaping

    # df[[,'AP_score']    

    # remove total row
    df.drop('T', level=1, inplace = True)
    # drop total exams column
    df.drop('TOTAL EXAMS', level=1, axis=1, inplace = True)

    return(df)

# add first level of index to blanks
def correct_levels(indx):
    first_level_name = ''
    new_indx = []

    for i in indx:
        if len(i[0]) > 0:
            first_level_name = i[0]
        new_indx.append((first_level_name, i[1]))

    return(pd.MultiIndex.from_tuples(new_indx, names = ['ethnicity','AP_score']))


## Washington 2013 All ##
wa_2013_all = pd.read_excel('../../data/College_Board/Washington_Summary_13.xls', sheet_name = 'All', skiprows=4, header=[0,1], 
        index_col = [0,1], usecols = 'B:AL', na_values = {'*',''}, skipfooter = 5)
clean_indexes(wa_2013_all)
wa_2013_all = clean_data(wa_2013_all)

# move mean score to second level of index
wa_2013_all.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2013_all.index])

# remove TOTAL
wa_2013_all.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2013_all.index])

wa_2013_all.index = correct_levels(wa_2013_all.index)

# stack subjects
wa_2013_all = wa_2013_all.stack('subject')

# move mean scores to separate df
tmp_df = wa_2013_all.copy(deep=True)

# remove mean score from working df
wa_2013_all.drop('MEAN SCORE', level=1, inplace = True)

# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]


wa_2013_all['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2013_all.index.get_level_values(0))):
    for subject in list(set(wa_2013_all.index.get_level_values(2))):
        try:
            wa_2013_all.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue

wa_2013_all['H2'] = 'D'
wa_2013_all['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2013_all['AP Exam Year'] = 2013
wa_2013_all['Table Name'] = 'WA-ALL CAND'
wa_2013_all['Geography'] = 'Washington'
wa_2013_all['Student Group'] = 'All Students'

wa_2013_all = wa_2013_all.reset_index()

wa_2013_all = wa_2013_all[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]

wa_2013_all.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2013_all.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2013_all.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2013_all.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2013 Females ##
student_group = 'Female Students'
# student_group = 'Male Students'
# student_group = 'All Students'
year = 2013
wa_2013_fem = pd.read_excel(
        '../../data/College_Board/Washington_Summary_13.xls', 
        sheet_name = 'Females', skiprows=4, header=[0,1], 
        index_col = [0,1], usecols = 'B:AL', na_values = {'*',''}, skipfooter = 5)

clean_indexes(wa_2013_fem)
wa_2013_fem = clean_data(wa_2013_fem)
# move mean score to second level of index
wa_2013_fem.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2013_fem.index])
# remove TOTAL
wa_2013_fem.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2013_fem.index])
wa_2013_fem.index = correct_levels(wa_2013_fem.index)
# stack subjects
wa_2013_fem = wa_2013_fem.stack('subject')
# move mean scores to separate df
tmp_df = wa_2013_fem.copy(deep=True)
# remove mean score from working df
wa_2013_fem.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2013_fem['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2013_fem.index.get_level_values(0))):
    for subject in list(set(wa_2013_fem.index.get_level_values(2))):
        try:
            wa_2013_fem.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2013_fem['H2'] = 'D'
wa_2013_fem['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2013_fem['AP Exam Year'] = year
wa_2013_fem['Table Name'] = 'WA-ALL CAND'
wa_2013_fem['Geography'] = 'Washington'
wa_2013_fem['Student Group'] = student_group
#
wa_2013_fem = wa_2013_fem.reset_index()
wa_2013_fem = wa_2013_fem[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2013_fem.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2013_fem.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2013_fem.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2013_fem.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2013 Males##
# student_group = 'Female Students'
student_group = 'Male Students'
# student_group = 'All Students'
year = 2013
wa_2013_mal = pd.read_excel(
        '../../data/College_Board/Washington_Summary_13.xls', 
        sheet_name = 'Males', skiprows=4, header=[0,1], 
        index_col = [0,1], usecols = 'B:AL', na_values = {'*',''}, skipfooter = 5)

clean_indexes(wa_2013_mal)
wa_2013_mal = clean_data(wa_2013_mal)
# move mean score to second level of index
wa_2013_mal.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2013_mal.index])
# remove TOTAL
wa_2013_mal.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2013_mal.index])
wa_2013_mal.index = correct_levels(wa_2013_mal.index)
# stack subjects
wa_2013_mal = wa_2013_mal.stack('subject')
# move mean scores to separate df
tmp_df = wa_2013_mal.copy(deep=True)
# remove mean score from working df
wa_2013_mal.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2013_mal['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2013_mal.index.get_level_values(0))):
    for subject in list(set(wa_2013_mal.index.get_level_values(2))):
        try:
            wa_2013_mal.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2013_mal['H2'] = 'D'
wa_2013_mal['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2013_mal['AP Exam Year'] = year
wa_2013_mal['Table Name'] = 'WA-ALL CAND'
wa_2013_mal['Geography'] = 'Washington'
wa_2013_mal['Student Group'] = student_group
#
wa_2013_mal = wa_2013_mal.reset_index()
wa_2013_mal = wa_2013_mal[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2013_mal.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2013_mal.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2013_mal.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2013_mal.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2014 All##
# student_group = 'Female Students'
# student_group = 'Male Students'
student_group = 'All Students'
year = 2014
wa_2014_all = pd.read_excel(
        '../../data/College_Board/Washington-Summary-2014.xlsx', 
        sheet_name = 'All', skiprows=4, header=[0,1], 
        index_col = [0,1], usecols = 'B:AL', na_values = {'*',''}, skipfooter = 5)

clean_indexes(wa_2014_all)
wa_2014_all = clean_data(wa_2014_all)
# move mean score to second level of index
wa_2014_all.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2014_all.index])
# remove TOTAL
wa_2014_all.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2014_all.index])
wa_2014_all.index = correct_levels(wa_2014_all.index)
# stack subjects
wa_2014_all = wa_2014_all.stack('subject')
# move mean scores to separate df
tmp_df = wa_2014_all.copy(deep=True)
# remove mean score from working df
wa_2014_all.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2014_all['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2014_all.index.get_level_values(0))):
    for subject in list(set(wa_2014_all.index.get_level_values(2))):
        try:
            wa_2014_all.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2014_all['H2'] = 'D'
wa_2014_all['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2014_all['AP Exam Year'] = year
wa_2014_all['Table Name'] = 'WA-ALL CAND'
wa_2014_all['Geography'] = 'Washington'
wa_2014_all['Student Group'] = student_group
#
wa_2014_all = wa_2014_all.reset_index()
wa_2014_all = wa_2014_all[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2014_all.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2014_all.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2014_all.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2014_all.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)


## Washington 2014 Females##
student_group = 'Female Students'
# student_group = 'Male Students'
# student_group = 'All Students'
year = 2014
wa_2014_female = pd.read_excel(
        '../../data/College_Board/Washington-Summary-2014.xlsx', 
        sheet_name = 'Females', skiprows=4, header=[0,1], 
        index_col = [0,1], usecols = 'B:AL', na_values = {'*',''}, skipfooter = 5)

clean_indexes(wa_2014_female)
wa_2014_female = clean_data(wa_2014_female)
# move mean score to second level of index
wa_2014_female.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2014_female.index])
# remove TOTAL
wa_2014_female.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2014_female.index])
wa_2014_female.index = correct_levels(wa_2014_female.index)
# stack subjects
wa_2014_female = wa_2014_female.stack('subject')
# move mean scores to separate df
tmp_df = wa_2014_female.copy(deep=True)
# remove mean score from working df
wa_2014_female.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2014_female['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2014_female.index.get_level_values(0))):
    for subject in list(set(wa_2014_female.index.get_level_values(2))):
        try:
            wa_2014_female.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2014_female['H2'] = 'D'
wa_2014_female['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2014_female['AP Exam Year'] = year
wa_2014_female['Table Name'] = 'WA-ALL CAND'
wa_2014_female['Geography'] = 'Washington'
wa_2014_female['Student Group'] = student_group
#
wa_2014_female = wa_2014_female.reset_index()
wa_2014_female = wa_2014_female[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2014_female.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2014_female.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2014_female.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2014_female.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2014 Males ##
# student_group = 'Female Students'
student_group = 'Male Students'
# student_group = 'All Students'
year = 2014
wa_2014_male = pd.read_excel(
        '../../data/College_Board/Washington-Summary-2014.xlsx', 
        sheet_name = 'Males', skiprows=4, header=[0,1], 
        index_col = [0,1], usecols = 'B:AL', na_values = {'*',''}, skipfooter = 5)

clean_indexes(wa_2014_male)
wa_2014_male = clean_data(wa_2014_male)
# move mean score to second level of index
wa_2014_male.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2014_male.index])
# remove TOTAL
wa_2014_male.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2014_male.index])
wa_2014_male.index = correct_levels(wa_2014_male.index)
# stack subjects
wa_2014_male = wa_2014_male.stack('subject')
# move mean scores to separate df
tmp_df = wa_2014_male.copy(deep=True)
# remove mean score from working df
wa_2014_male.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2014_male['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2014_male.index.get_level_values(0))):
    for subject in list(set(wa_2014_male.index.get_level_values(2))):
        try:
            wa_2014_male.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2014_male['H2'] = 'D'
wa_2014_male['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2014_male['AP Exam Year'] = year
wa_2014_male['Table Name'] = 'WA-ALL CAND'
wa_2014_male['Geography'] = 'Washington'
wa_2014_male['Student Group'] = student_group
#
wa_2014_male = wa_2014_male.reset_index()
wa_2014_male = wa_2014_male[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2014_male.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2014_male.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2014_male.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2014_male.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2015 All##
# student_group = 'Female Students'
# student_group = 'Male Students'
student_group = 'All Students'
year = 2015
wa_2015_all = pd.read_excel(
        '../../data/College_Board/washington-summary-2015.xlsx', 
        sheet_name = 'All', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AN', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 6)

clean_indexes(wa_2015_all)
wa_2015_all = clean_data(wa_2015_all)
# move mean score to second level of index
wa_2015_all.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2015_all.index])
# remove TOTAL
wa_2015_all.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2015_all.index])
wa_2015_all.index = correct_levels(wa_2015_all.index)
# stack subjects
wa_2015_all = wa_2015_all.stack('subject')
# move mean scores to separate df
tmp_df = wa_2015_all.copy(deep=True)
# remove mean score from working df
wa_2015_all.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2015_all['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2015_all.index.get_level_values(0))):
    for subject in list(set(wa_2015_all.index.get_level_values(2))):
        try:
            wa_2015_all.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2015_all['H2'] = 'D'
wa_2015_all['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2015_all['AP Exam Year'] = year
wa_2015_all['Table Name'] = 'WA-ALL CAND'
wa_2015_all['Geography'] = 'Washington'
wa_2015_all['Student Group'] = student_group
#
wa_2015_all = wa_2015_all.reset_index()
wa_2015_all = wa_2015_all[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2015_all.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2015_all.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2015_all.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2015_all.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2015 Female ##
student_group = 'Female Students'
# student_group = 'Male Students'
# student_group = 'All Students'
year = 2015
wa_2015_female = pd.read_excel(
        '../../data/College_Board/washington-summary-2015.xlsx', 
        sheet_name = 'Females', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AN', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 6)

clean_indexes(wa_2015_female)
wa_2015_female = clean_data(wa_2015_female)
# move mean score to second level of index
wa_2015_female.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2015_female.index])
# remove TOTAL
wa_2015_female.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2015_female.index])
wa_2015_female.index = correct_levels(wa_2015_female.index)
# stack subjects
wa_2015_female = wa_2015_female.stack('subject')
# move mean scores to separate df
tmp_df = wa_2015_female.copy(deep=True)
# remove mean score from working df
wa_2015_female.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2015_female['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2015_female.index.get_level_values(0))):
    for subject in list(set(wa_2015_female.index.get_level_values(2))):
        try:
            wa_2015_female.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2015_female['H2'] = 'D'
wa_2015_female['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2015_female['AP Exam Year'] = year
wa_2015_female['Table Name'] = 'WA-ALL CAND'
wa_2015_female['Geography'] = 'Washington'
wa_2015_female['Student Group'] = student_group
#
wa_2015_female = wa_2015_female.reset_index()
wa_2015_female = wa_2015_female[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2015_female.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2015_female.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2015_female.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2015_female.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2015 Male ##
# student_group = 'Female Students'
student_group = 'Male Students'
# student_group = 'All Students'
year = 2015
wa_2015_male = pd.read_excel(
        '../../data/College_Board/washington-summary-2015.xlsx', 
        sheet_name = 'Males', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AN', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 6)

clean_indexes(wa_2015_male)
wa_2015_male = clean_data(wa_2015_male)
# move mean score to second level of index
wa_2015_male.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2015_male.index])
# remove TOTAL
wa_2015_male.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2015_male.index])
wa_2015_male.index = correct_levels(wa_2015_male.index)
# stack subjects
wa_2015_male = wa_2015_male.stack('subject')
# move mean scores to separate df
tmp_df = wa_2015_male.copy(deep=True)
# remove mean score from working df
wa_2015_male.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2015_male['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2015_male.index.get_level_values(0))):
    for subject in list(set(wa_2015_male.index.get_level_values(2))):
        try:
            wa_2015_male.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2015_male['H2'] = 'D'
wa_2015_male['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2015_male['AP Exam Year'] = year
wa_2015_male['Table Name'] = 'WA-ALL CAND'
wa_2015_male['Geography'] = 'Washington'
wa_2015_male['Student Group'] = student_group
#
wa_2015_male = wa_2015_male.reset_index()
wa_2015_male = wa_2015_male[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2015_male.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2015_male.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2015_male.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2015_male.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)


## Washington 2016 All ##
# student_group = 'Female Students'
# student_group = 'Male Students'
student_group = 'All Students'
year = 2016
wa_2016_all = pd.read_excel(
        '../../data/College_Board/washington-summary-2016.xlsx', 
        sheet_name = 'All', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AO', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 7)

clean_indexes(wa_2016_all)
wa_2016_all = clean_data(wa_2016_all)
# move mean score to second level of index
wa_2016_all.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2016_all.index])
# remove TOTAL
wa_2016_all.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2016_all.index])
wa_2016_all.index = correct_levels(wa_2016_all.index)
# stack subjects
wa_2016_all = wa_2016_all.stack('subject')
# move mean scores to separate df
tmp_df = wa_2016_all.copy(deep=True)
# remove mean score from working df
wa_2016_all.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2016_all['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2016_all.index.get_level_values(0))):
    for subject in list(set(wa_2016_all.index.get_level_values(2))):
        try:
            wa_2016_all.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2016_all['H2'] = 'D'
wa_2016_all['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2016_all['AP Exam Year'] = year
wa_2016_all['Table Name'] = 'WA-ALL CAND'
wa_2016_all['Geography'] = 'Washington'
wa_2016_all['Student Group'] = student_group
#
wa_2016_all = wa_2016_all.reset_index()
wa_2016_all = wa_2016_all[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2016_all.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2016_all.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2016_all.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2016_all.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)


## Washington 2016 Female ##
student_group = 'Female Students'
# student_group = 'Male Students'
# student_group = 'All Students'
year = 2016
wa_2016_female = pd.read_excel(
        '../../data/College_Board/washington-summary-2016.xlsx', 
        sheet_name = 'Females', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AO', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 7)

clean_indexes(wa_2016_female)
wa_2016_female = clean_data(wa_2016_female)
# move mean score to second level of index
wa_2016_female.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2016_female.index])
# remove TOTAL
wa_2016_female.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2016_female.index])
wa_2016_female.index = correct_levels(wa_2016_female.index)
# stack subjects
wa_2016_female = wa_2016_female.stack('subject')
# move mean scores to separate df
tmp_df = wa_2016_female.copy(deep=True)
# remove mean score from working df
wa_2016_female.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2016_female['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2016_female.index.get_level_values(0))):
    for subject in list(set(wa_2016_female.index.get_level_values(2))):
        try:
            wa_2016_female.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2016_female['H2'] = 'D'
wa_2016_female['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2016_female['AP Exam Year'] = year
wa_2016_female['Table Name'] = 'WA-ALL CAND'
wa_2016_female['Geography'] = 'Washington'
wa_2016_female['Student Group'] = student_group
#
wa_2016_female = wa_2016_female.reset_index()
wa_2016_female = wa_2016_female[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2016_female.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2016_female.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2016_female.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2016_female.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2016 Male ##
# student_group = 'Female Students'
student_group = 'Male Students'
# student_group = 'All Students'
year = 2016
wa_2016_male = pd.read_excel(
        '../../data/College_Board/washington-summary-2016.xlsx', 
        sheet_name = 'Males', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AO', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 7)

clean_indexes(wa_2016_male)
wa_2016_male = clean_data(wa_2016_male)
# move mean score to second level of index
wa_2016_male.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2016_male.index])
# remove TOTAL
wa_2016_male.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2016_male.index])
wa_2016_male.index = correct_levels(wa_2016_male.index)
# stack subjects
wa_2016_male = wa_2016_male.stack('subject')
# move mean scores to separate df
tmp_df = wa_2016_male.copy(deep=True)
# remove mean score from working df
wa_2016_male.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2016_male['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2016_male.index.get_level_values(0))):
    for subject in list(set(wa_2016_male.index.get_level_values(2))):
        try:
            wa_2016_male.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2016_male['H2'] = 'D'
wa_2016_male['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2016_male['AP Exam Year'] = year
wa_2016_male['Table Name'] = 'WA-ALL CAND'
wa_2016_male['Geography'] = 'Washington'
wa_2016_male['Student Group'] = student_group
#
wa_2016_male = wa_2016_male.reset_index()
wa_2016_male = wa_2016_male[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2016_male.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2016_male.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2016_male.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2016_male.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2017 All ##
# student_group = 'Female Students'
# student_group = 'Male Students'
student_group = 'All Students'
year = 2017
wa_2017_all = pd.read_excel(
        '../../data/College_Board/washington-summary-2017.xlsx', 
        sheet_name = 'All', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AP', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 8)

clean_indexes(wa_2017_all)
wa_2017_all = clean_data(wa_2017_all)
# move mean score to second level of index
wa_2017_all.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2017_all.index])
# remove TOTAL
wa_2017_all.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2017_all.index])
wa_2017_all.index = correct_levels(wa_2017_all.index)
# stack subjects
wa_2017_all = wa_2017_all.stack('subject')
# move mean scores to separate df
tmp_df = wa_2017_all.copy(deep=True)
# remove mean score from working df
wa_2017_all.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2017_all['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2017_all.index.get_level_values(0))):
    for subject in list(set(wa_2017_all.index.get_level_values(2))):
        try:
            wa_2017_all.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2017_all['H2'] = 'D'
wa_2017_all['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2017_all['AP Exam Year'] = year
wa_2017_all['Table Name'] = 'WA-ALL CAND'
wa_2017_all['Geography'] = 'Washington'
wa_2017_all['Student Group'] = student_group
#
wa_2017_all = wa_2017_all.reset_index()
wa_2017_all = wa_2017_all[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2017_all.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2017_all.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2017_all.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2017_all.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2017 Females ##
# student_group = 'All Students'
student_group = 'Female Students'
# student_group = 'Male Students'
year = 2017
wa_2017_female = pd.read_excel(
        '../../data/College_Board/washington-summary-2017.xlsx', 
        sheet_name = 'Females', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AP', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 8)

clean_indexes(wa_2017_female)
wa_2017_female = clean_data(wa_2017_female)
# move mean score to second level of index
wa_2017_female.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2017_female.index])
# remove TOTAL
wa_2017_female.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2017_female.index])
wa_2017_female.index = correct_levels(wa_2017_female.index)
# stack subjects
wa_2017_female = wa_2017_female.stack('subject')
# move mean scores to separate df
tmp_df = wa_2017_female.copy(deep=True)
# remove mean score from working df
wa_2017_female.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2017_female['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2017_female.index.get_level_values(0))):
    for subject in list(set(wa_2017_female.index.get_level_values(2))):
        try:
            wa_2017_female.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2017_female['H2'] = 'D'
wa_2017_female['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2017_female['AP Exam Year'] = year
wa_2017_female['Table Name'] = 'WA-ALL CAND'
wa_2017_female['Geography'] = 'Washington'
wa_2017_female['Student Group'] = student_group
#
wa_2017_female = wa_2017_female.reset_index()
wa_2017_female = wa_2017_female[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2017_female.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2017_female.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2017_female.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2017_female.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)


## Washington 2017 Males ##
# student_group = 'All Students'
# student_group = 'Female Students'
student_group = 'Male Students'
year = 2017
wa_2017_male = pd.read_excel(
        '../../data/College_Board/washington-summary-2017.xlsx', 
        sheet_name = 'Males', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AP', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 8)

clean_indexes(wa_2017_male)
wa_2017_male = clean_data(wa_2017_male)
# move mean score to second level of index
wa_2017_male.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2017_male.index])
# remove TOTAL
wa_2017_male.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2017_male.index])
wa_2017_male.index = correct_levels(wa_2017_male.index)
# stack subjects
wa_2017_male = wa_2017_male.stack('subject')
# move mean scores to separate df
tmp_df = wa_2017_male.copy(deep=True)
# remove mean score from working df
wa_2017_male.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2017_male['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2017_male.index.get_level_values(0))):
    for subject in list(set(wa_2017_male.index.get_level_values(2))):
        try:
            wa_2017_male.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2017_male['H2'] = 'D'
wa_2017_male['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2017_male['AP Exam Year'] = year
wa_2017_male['Table Name'] = 'WA-ALL CAND'
wa_2017_male['Geography'] = 'Washington'
wa_2017_male['Student Group'] = student_group
#
wa_2017_male = wa_2017_male.reset_index()
wa_2017_male = wa_2017_male[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2017_male.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2017_male.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2017_male.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2017_male.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)


## Washington 2018 All ##
student_group = 'All Students'
# student_group = 'Female Students'
# student_group = 'Male Students'
year = 2018
wa_2018_all = pd.read_excel(
        '../../data/College_Board/washington-summary-2018.xlsx', 
        sheet_name = 'All', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AP', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 6)

clean_indexes(wa_2018_all)
wa_2018_all = clean_data(wa_2018_all)
# move mean score to second level of index
wa_2018_all.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2018_all.index])
# remove TOTAL
wa_2018_all.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2018_all.index])
wa_2018_all.index = correct_levels(wa_2018_all.index)
# stack subjects
wa_2018_all = wa_2018_all.stack('subject')
# move mean scores to separate df
tmp_df = wa_2018_all.copy(deep=True)
# remove mean score from working df
wa_2018_all.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2018_all['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2018_all.index.get_level_values(0))):
    for subject in list(set(wa_2018_all.index.get_level_values(2))):
        try:
            wa_2018_all.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2018_all['H2'] = 'D'
wa_2018_all['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2018_all['AP Exam Year'] = year
wa_2018_all['Table Name'] = 'WA-ALL CAND'
wa_2018_all['Geography'] = 'Washington'
wa_2018_all['Student Group'] = student_group
#
wa_2018_all = wa_2018_all.reset_index()
wa_2018_all = wa_2018_all[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2018_all.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2018_all.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2018_all.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2018_all.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Washington 2018 Female ##
# student_group = 'All Students'
student_group = 'Female Students'
# student_group = 'Male Students'
year = 2018
wa_2018_female = pd.read_excel(
        '../../data/College_Board/washington-summary-2018.xlsx', 
        sheet_name = 'Females', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AP', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 6)

clean_indexes(wa_2018_female)
wa_2018_female = clean_data(wa_2018_female)
# move mean score to second level of index
wa_2018_female.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2018_female.index])
# remove TOTAL
wa_2018_female.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2018_female.index])
wa_2018_female.index = correct_levels(wa_2018_female.index)
# stack subjects
wa_2018_female = wa_2018_female.stack('subject')
# move mean scores to separate df
tmp_df = wa_2018_female.copy(deep=True)
# remove mean score from working df
wa_2018_female.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2018_female['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2018_female.index.get_level_values(0))):
    for subject in list(set(wa_2018_female.index.get_level_values(2))):
        try:
            wa_2018_female.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2018_female['H2'] = 'D'
wa_2018_female['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2018_female['AP Exam Year'] = year
wa_2018_female['Table Name'] = 'WA-ALL CAND'
wa_2018_female['Geography'] = 'Washington'
wa_2018_female['Student Group'] = student_group
#
wa_2018_female = wa_2018_female.reset_index()
wa_2018_female = wa_2018_female[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2018_female.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2018_female.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2018_female.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2018_female.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)


## Washington 2018 Male ##
# student_group = 'All Students'
# student_group = 'Female Students'
student_group = 'Male Students'
year = 2018
wa_2018_male = pd.read_excel(
        '../../data/College_Board/washington-summary-2018.xlsx', 
        sheet_name = 'Males', 
        skiprows=4, 
        header=[0,1], 
        usecols = 'B:AP', 
        index_col = [0,1], 
        na_values = {'*',''}, 
        skipfooter = 6)

clean_indexes(wa_2018_male)
wa_2018_male = clean_data(wa_2018_male)
# move mean score to second level of index
wa_2018_male.index = pd.MultiIndex.from_tuples(
        [('', 'MEAN SCORE') if x[0] == 'MEAN SCORE' else (x[0], x[1]) for x in wa_2018_male.index])
# remove TOTAL
wa_2018_male.index = pd.MultiIndex.from_tuples(
        [('', x[1]) if x[0] == 'TOTAL' else (x[0], x[1]) for x in wa_2018_male.index])
wa_2018_male.index = correct_levels(wa_2018_male.index)
# stack subjects
wa_2018_male = wa_2018_male.stack('subject')
# move mean scores to separate df
tmp_df = wa_2018_male.copy(deep=True)
# remove mean score from working df
wa_2018_male.drop('MEAN SCORE', level=1, inplace = True)
# remove all but mean scores from temp df
# wa_2013.loc[[,'MEAN SCORE']]
# tmp_df.loc[(slice(None),'MEAN SCORE'),:]
idx = pd.IndexSlice
tmp_df = tmp_df.loc[idx[:, 'MEAN SCORE'], :]
# add mean score for correct index to mean score column
wa_2018_male['MEAN SCORE'] = np.nan
for ethnicity in list(set(wa_2018_male.index.get_level_values(0))):
    for subject in list(set(wa_2018_male.index.get_level_values(2))):
        try:
            wa_2018_male.loc[idx[ethnicity, :, subject],'MEAN SCORE'] = tmp_df.loc[
                    idx[ethnicity, :, subject],:].values[0][0]
        except IndexError:
            continue
#
wa_2018_male['H2'] = 'D'
wa_2018_male['MEASURE NAME'] = 'SCHOOL AP SCORE DISTRIBUTIONS BY TOTAL AND ETHNIC GROUP'
wa_2018_male['AP Exam Year'] = year
wa_2018_male['Table Name'] = 'WA-ALL CAND'
wa_2018_male['Geography'] = 'Washington'
wa_2018_male['Student Group'] = student_group
#
wa_2018_male = wa_2018_male.reset_index()
wa_2018_male = wa_2018_male[['H2','MEASURE NAME', 'AP Exam Year', 'Table Name', 'Geography', 'Student Group', 'ethnicity', 'AP_score', 'subject', 'NUMBER OF STUDENTS FOR EACH EXAMINATION', 'MEAN SCORE']]
#
wa_2018_male.rename(columns={'ethnicity': 'Subgroup'}, inplace=True)
wa_2018_male.rename(columns={'AP_score': 'AP Score'}, inplace=True)
wa_2018_male.rename(columns={'subject': 'Subject'}, inplace=True)
wa_2018_male.rename(columns={'NUMBER OF STUDENTS FOR EACH EXAMINATION': 'Student Count'}, inplace=True)

## Staple together and write output
big_df = pd.concat([wa_2013_all, wa_2013_fem, wa_2013_mal, 
                    wa_2014_all, wa_2014_female, wa_2014_male,
                    wa_2015_all, wa_2015_female, wa_2015_male,
                    wa_2016_all, wa_2016_female, wa_2016_male,
                    wa_2017_all, wa_2017_female, wa_2017_male,
                    wa_2018_all, wa_2018_female, wa_2018_male
                    ], ignore_index = True)
writer = pd.ExcelWriter('../../data/College_Board/output.xlsx')
big_df.to_excel(writer, index=False)
writer.save()



# Washington_Summary_12.xls    washington-summary-2015.xlsx
# NATIONAL_Summary_09.xls      WASHINGTON_Summary_08.xls    Washington_Summary_13.xls    washington-summary-2016.xlsx
# NATIONAL_Summary_10.xls      WASHINGTON_Summary_09.xls    national-summary-2015.xlsx   washington-summary-2017.xlsx
# NATIONAL_Summary_11.xls      WASHINGTON_Summary_10.xls    national-summary-2016.xlsx   washington-summary-2018.xlsx
# National-Summary-2014.xlsx   WASHINGTON_Summary_11.xls    national-summary-2017.xlsx
# National_Summary_12.xls      Washington-Summary-2014.xlsx national-summary-2018.xlsx

