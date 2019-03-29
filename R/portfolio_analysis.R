#############################################################
## (In progress) Simple Portfolio Analysis
## bcutrell13@gmail.com - March 2019
#############################################################

##############################
# 0 - Load librairies
##############################
library(quantmod)
library(PerformanceAnalytics)

############################## 
# 1 - Source data
##############################

# TODO convert to rds file
# dataPath <- "C:/some_directory/some_sub_directory/"
# dataFile <- "some_functions.R"
# source(paste0(dataPath,dataFile))

secs <- c('ITOT', 'IXUS', 'AGG')

for (sec in secs) {
  getSymbols(sec)
}

##############################
# 2 - Code
##############################
prices <- cbind(ITOT$ITOT.Adjusted, IXUS$IXUS.Adjusted)

colnames(prices) <- c('ITOT', 'IXUS')

returns <- Return.calculate(prices)

# Create the weights
eq_weights <- c(0.5, 0.5)

# Create a portfolio using buy and hold
pf_bh <- Return.portfolio(R = returns, weights = eq_weights)

# Create a portfolio rebalancing monthly 
pf_rebal <- Return.portfolio(R = returns, weights = eq_weights, rebalance_on="months")

par(mfrow = c(2, 1), mar = c(2, 4, 2, 2))
plot.zoo(pf_bh)
plot.zoo(pf_rebal)

