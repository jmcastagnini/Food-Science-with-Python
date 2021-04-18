import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri# Defining the R script and loading the instance in Python
pandas2ri.activate()

def anova1(df,treatment,col,sheet_name=0,factor='categoric',sort_df=False):
    """df: dataframe with data as a string or as a pandas DataFrame
       treatment: column number in R (starting in 1) where the treatment is located, usually is the 0 column
       col: initial column in Python (starting in 0) where result analysis are located
       sheet_name: only used for excel files, default value is 0 (First sheet of excel), Strings are used for sheet names. Integers are used in zero-indexed sheet positions
       factor: by default is categoric; the other option is numeric
       sort_df: by default is False. If you want to order the data frame by treatment column, then change to True
    """
    
    # Opening the Data frame
    if isinstance(df, pd.DataFrame):
        df = df
    else:
        extension = os.path.splitext(df)[1][1:]
        if extension == 'xlsx' or extension == 'xls':
            df = pd.read_excel(io=df, sheet_name=sheet_name)
        elif extension =='csv':
            df = pd.read_csv(df, sep=';')
        else:
            return 'extension not supported'
    
    column = list(df.columns.values)
    
    if sort_df == True:
        df.sort_values(by=column[treatment-1],inplace=True)



    # Defining the R script and loading the instance in Python
    r = robjects.r
    r['source']('./analysis_variance.R')

    # Loading the function we have defined in R.
    analysis_variance_r = robjects.globalenv['analysis_variance']

    # Reading and processing data
    
    df_result = {}  # initialize empty dictionary
    df_r = pandas2ri.py2rpy(df)

    # Statistical Results
    for analysis in column[col:len(column)]:
        #Invoking the R function and getting the result
        df_result_r = analysis_variance_r(df_r, analysis,treatment,factor)
        #Converting it back to a pandas dataframe
        df_result["{}".format(analysis)] = df_result_r

    f,p = stats.f_oneway(*[np.array(df[df[column[treatment-1]]==item].iloc[:,col:len(column)]) for item in df[column[treatment-1]].drop_duplicates()])
    
    i= 0
    for key in df_result.keys():
        df_result[key].loc[len(df_result[key].index)] = ['{:.3f}'.format(f[i]),'-']
        df_result[key].rename(index={len(df_result[key].index)-1:'f'},inplace=True)
        df_result[key].loc[len(df_result[key].index)] = ['{0:.3f}'.format(p[i]),'-']
        df_result[key].rename(index={len(df_result[key].index)-1:'p'},inplace=True)
        i+=1
        
    return(df_result)