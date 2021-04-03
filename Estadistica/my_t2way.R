my_t2way <- function(df1){
	library(WRS2)
    df <- read.csv2(df1,header = TRUE, sep=',')
    df[ , c('attractiveness')] <- as.numeric(df[ , c('attractiveness')])
    df[ , c('alcohol')] <- as.factor(df[ , c('alcohol')])
    df[ , c('gender')] <- as.factor(df[ , c('gender')])
    f <- t2way(attractiveness ~ gender*alcohol, data = df) 
    df1 = data.frame(factor=c('gender','alcohol','gender:alcohol'),
                     value = c(f$Qa,f$Qb,f$Qab),
                    p.value = c(f$A.p.value,f$B.p.value,f$AB.p.value))
    return(df1)
}