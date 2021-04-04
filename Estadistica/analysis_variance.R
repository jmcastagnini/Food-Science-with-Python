analysis_variance <- function(df_r,analysis,treatment,factor){
	library(agricolae)
    #A <- read.csv2(df,header = TRUE, dec = ".")  # Open the file and read the data 
    A <- df_r
    
    # Change the data type
    A[ , c(analysis)] <- as.numeric(A[ , c(analysis)]) 
    if (factor == 'numeric') {
        A[ , c(treatment)] <- as.numeric(A[ , c(treatment)])
    } else {
        A[ , c(treatment)] <- as.factor(A[ , c(treatment)])
    }
    
    # Make a linear model for the Post-hoc test
    m1 <- aov(as.formula(paste(analysis, '~',colnames(A)[treatment])), data = A) 
    
    # Make the analysis of variance by Groups=Treatments
    out1 <- HSD.test(m1,colnames(A)[treatment],console = FALSE)  
    df_treatments <- out1$groups
    
    # Extract the name of the treatments to re-order=sort
    row_order <- row.names(df_treatments)  
    
    # Sort Data Frame with Base R (order Function) and set the type of data (as.numeric or as.factor)
    if (factor == 'numeric') {
        tidy_df <- df_treatments[order(as.numeric(row_order)), ]
    } else {
        tidy_df <- df_treatments[order(as.character(row_order)), ]
    }
    
    mean_std_df <- out1$means[ , c(analysis, "std")]  # Data frame with medias and standard deviation
    
    tidy_df[ , c(analysis)] <- paste(round((mean_std_df[ , c(analysis)]),digits = 3),"±",round((mean_std_df$std),digits = 3))
    
    colnames(tidy_df)[colnames(tidy_df) == "groups"] <- paste0(analysis,'-','groups')
    
    return(tidy_df)
}