import os
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri# Defining the R script and loading the instance in Python
pandas2ri.activate()

def anova1(df,treatment,col,sheet_name=0,factor='categoric'):
    """df: dataframe with data as a string
       treatment: column number in R (starting in 1) where the treatment is located, usually is the 0 column
       col: initial column in Python (starting in 0) where result analysis are located
       sheet_name: only used for excel files, default value is 0 (First sheet of excel), Strings are used for sheet names. Integers are used in zero-indexed sheet positions
       factor: by default is categoric; the other option is numeric
    """
    
    # Opening the Data frame
    extension = os.path.splitext(df)[1][1:]
    if extension == 'xlsx' or extension == 'xls':
        df = pd.read_excel(io=df, sheet_name=sheet_name)
    elif extension =='csv':
        df = pd.read_csv(df, sep=';')
    else:
        return 'extension not supported'
        
    
    # Defining the R script and loading the instance in Python
    r = robjects.r
    r['source']('./analysis_variance.R')

    # Loading the function we have defined in R.
    analysis_variance_r = robjects.globalenv['analysis_variance']

    # Reading and processing data
    column = list(df.columns.values)
    df_dict = {}  # initialize empty dictionary
    df_r = pandas2ri.py2rpy(df)

    # Statistical Results
    for analysis in column[col:len(column)]:
        #Invoking the R function and getting the result
        df_result_r = analysis_variance_r(df_r, analysis,treatment,factor)
        #Converting it back to a pandas dataframe
        df_dict["{}".format(analysis)] = df_result_r
    return(df_dict)