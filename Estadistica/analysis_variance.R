analysis_variance <- function(df_r,analysis,treatment){
	library(agricolae)
    #A <- read.csv2(df,header = TRUE, dec = ".")  # Open the file and read the data 
    A <- df_r
    A[ , c(analysis)] <- as.numeric(A[ , c(analysis)])  # Change the data type to numeric
    m1 <- aov(as.formula(paste(analysis, '~',colnames(A)[treatment])), data = A)  # Make a linear model for the Post-hoc test
    out1 <- HSD.test(m1,colnames(A)[treatment],console = FALSE)  # Make the analysis of variance by Groups=Treatments
    df_treatments <- out1$groups
    row_order <- row.names(df_treatments)  # Extract the name of the treatments to re-order=sort
    tidy_df <- df_treatments[order(as.character(row_order)), ]  # Sort Data Frame with Base R (order Function)
    mean_std_df <- out1$means[ , c(analysis, "std")]  # Data frame with medias and standard deviation
    tidy_df[ , c(analysis)] <- paste(round((mean_std_df[ , c(analysis)]),digits = 3),"±",round((mean_std_df$std),digits = 3))
    colnames(tidy_df)[colnames(tidy_df) == "groups"] <- paste0(analysis,'-','groups')
    return(tidy_df)
}