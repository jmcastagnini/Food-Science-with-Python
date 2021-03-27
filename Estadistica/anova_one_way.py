import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri# Defining the R script and loading the instance in Python

def anova1(df,col,treatment):
    """df: dataframe with data as a string
       treatment: column number in R (starting in 1) where the treatment is located, usually is the 0 column
       col: initial column in Python (starting in 0) where result analysis are located  """
    
    # Defining the R script and loading the instance in Python
    r = robjects.r
    r['source']('./analysis_variance.R')

    # Loading the function we have defined in R.
    analysis_variance_r = robjects.globalenv['analysis_variance']

    # Reading and processing data
    df1 = pd.read_csv(df, sep=';') # File con i risultati
    column = list(df1.columns.values)
    df_dict = {}  # initialize empty dictionary

    # Statistical Results
    for analysis in column[col:len(column)]:
        #Invoking the R function and getting the result
        df_result_r = analysis_variance_r(df, analysis,treatment)
        #Converting it back to a pandas dataframe
        df_dict["{}".format(analysis)] = pandas2ri.rpy2py(df_result_r)
    return(df_dict)