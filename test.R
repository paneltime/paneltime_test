require(rugarch) || {install.packages("rugarch"); require(rugarch)}
library(readr)

df <- data.frame(matrix(ncol = 14, nrow = 0))
x <- c("mu","ar1","ar2","ma1","ma2","mxreg1","mxreg2", 
       "omega","alpha1", "alpha2", "beta1", "beta2", "LL", "time")
colnames(df) <- x


for (i in 1:1000) {
  print(i)
  path = paste("B:/Forskning/Papers/paneltime/paneltime_test/simulations/data", 
               i-1, ".csv", sep="")
  data <- read.csv(path, header=TRUE)
  
  ptm <- proc.time()
  garchMod <- ugarchspec(
    variance.model=list(model="sGARCH",
                        garchOrder=c(2,2)),
    
    
    mean.model=list(armaOrder=c(2,2),
                    include.mean=TRUE,
                    external.regressors=data.matrix(subset(data, select=c("X0","X1")))
    ), 
    distribution.model="norm"
  )
  garchFit <- ugarchfit(spec=garchMod, data=data$Y)
  print(garchFit)

  
  coefs=coef(garchFit)
  
  # Check if garchFit is NULL
  if (is.null(coefs)) {
    # Fill coefs with NA values, assuming df has k columns
    # Names of the coefficients from a successful garchFit
    coef_names <- c("mu", "ar1", "ar2", "ma1", "ma2", "mxreg1", "mxreg2", "omega", "alpha1", "alpha2", "beta1", "beta2")
    # Create a named vector with all values as NA
    coefs <- setNames(rep(NA, length(coef_names)), coef_names)

  }
  
  coefs = append(coefs,c("LL" = likelihood(garchFit), "time"= proc.time() - ptm))
  df[i,]=coefs
}

write.table(df,"B:/Forskning/Papers/paneltime/paneltime_test/rresults.csv", sep=';')
