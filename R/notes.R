#############################################################
## A bunch of unorganized notes from my datacamp courses
## bcutrell13@gmail.com - March 2019
#############################################################

# some good resources ->
# https://rstudio-pubs-static.s3.amazonaws.com/78839_afca73ae18194eaf8f1b86d399dde969.html
# http://www.thertrader.com/

# Can we improve risk sensitivity of VaR and ES estimates?
# Filtered historical simulation, GARCH models, EWMA volatility filters

library(quantmod)

# Get data
getSymbols('IVV')

# Plot % return
diff_ivv <- diff(IVV$IVV.Adjusted)

head(diff_ivv)

plot(diff_ivv)

# Plot the original random_walk data
ts.plot(random_walk)

# Use abline(0, ...) to add time trend to the figure
abline(0,int_wn)

model_wn <- arima(rw_diff, order=c(0,0,0))

# Simulate an AR model with 0.5 slope
x <- arima.sim(model = list(ar=0.5), n = 100)

# Simulate an AR model with 0.9 slope
y <- arima.sim(model = list(ar=0.9), n = 100)

# Simulate an AR model with -0.75 slope
z <- arima.sim(model = list(ar=-0.75), n = 100)

# Plot your simulated data
plot.ts(cbind(x, y, z))

# Simulate and plot RW model
z <- arima.sim(model = list(order = c(0, 1, 0)), n = 200)

# Fit the MA model to Nile
MA <- arima(Nile, order = c(0,0,1))
print(MA)

# Plot Nile and MA_fit
ts.plot(Nile)
MA_fit <- Nile - resid(MA)
points(MA_fit, type = "l", col = 2, lty = 2)

white noise (WN), random walk (RW), autoregressive (AR), and simple moving average (MA)

Plot A shows autocorrelation for the first lag only, which is consistent with the expectations of the MA model. Plot B shows dissipating autocorrelation across several lags, consistent with the AR model. Plot C is consistent with a RW model with considerable autocorrelation for many lags. Finally. Plot D shows virtually no autocorrelation with any lags, consistent with a WN model. Understanding the logic behind these ACF plots is crucial for understanding how each model operates.

# Generate and plot white noise
WN <- arima.sim(model=list(order=(c(0,0,0))), n=200)
plot(WN)

# Generate and plot an MA(1) with parameter .9
MA <- arima.sim(model = list(order = c(0, 0, 1), ma = .9 ), n = 200)
plot(MA)

# Generate and plot an AR(2) with parameters 1.5 and -.75
AR <- arima.sim(model = list(order= c(2,0,0), ar=c(1.5, -0.75)), n = 200)
plot(AR)

# Generate 100 observations from the AR(1) model
x <- arima.sim(model = list(order = c(1, 0, 0), ar = .9), n = 100)

# Plot the generated data
plot(x)

# Plot the sample P/ACF pair
acf2(x)

# Fit an AR(1) to the data and examine the t-table
sarima(x, 1,0,0)

# You should always examine the residuals because the model assumes the errors are Gaussian white noise.


library(quantmod)
library(tidyverse)
library(ggplot2)

# https://github.com/tidyverse/tidyverse/issues/132
# https://github.com/r-lib/xml2/issues/232

# Get data
getSymbols('IVV')

# Plot % return
diff_ivv <- diff(IVV$IVV.Adjusted)

# plot <- plot(IVV$IVV.Adjusted)

plot <- ggplot(IVV$IVV.Adjusted)
ggsave('x.png', plot)
# http://www.thertrader.com/

# Generate monthly difference in unemployment
unemployment$us_monthlydiff <- diff(unemployment$us, lag = 1, differences = 1)

# Generate yearly difference in unemployment
unemployment$us_yearlydiff <- diff(unemployment$us, lag = 12, differences = 1)

# Plot US unemployment and annual difference
par(mfrow = c(2,1))
plot.xts(unemployment$us)
plot.xts(unemployment$us_yearlydiff, type = "h")

# Convert the daily frequency of sp500 to monthly frequency: sp500_monthly
sp500_monthly <- to.monthly(sp500)

# Print the first six rows of sp500_monthly
head(sp500_monthly, 6)

# Create sp500_returns using Return.calculate using the closing prices
sp500_returns <- Return.calculate(sp500_monthly$sp500.Close)

# Time series plot
plot.zoo(sp500_returns)

# Produce the year x month table
table.CalendarReturns(sp500_returns)

# Compute the annualized mean
Return.annualized(sp500_returns)

# Compute the annualized standard deviation
StdDev.annualized(sp500_returns)

# Compute the annualized Sharpe ratio: ann_sharpe
ann_sharpe <- Return.annualized(sp500_returns)/StdDev.annualized(sp500_returns)

# Compute all of the above at once using table.AnnualizedReturns()
table.AnnualizedReturns(sp500_returns)

# Calculate the mean, volatility, and Sharpe ratio of sp500_returns
returns_ann <- Return.annualized(sp500_returns)
sd_ann <- StdDev.annualized(sp500_returns)
sharpe_ann <- SharpeRatio.annualized(sp500_returns,rf)

# Plotting the 12-month rolling annualized mean
chart.RollingPerformance(R = sp500_returns, width = 12, FUN = "Return.annualized")

# Plotting the 12-month rolling annualized standard deviation
chart.RollingPerformance(R = sp500_returns, width = 12, FUN = "StdDev.annualized")

# Plotting the 12-month rolling annualized Sharpe ratio
chart.RollingPerformance(R = sp500_returns, width = 12, FUN = "SharpeRatio.annualized", Rf=rf)

# Fill in window for 2008
sp500_2008 <- window(sp500_returns, start = "2008-01-01", end = "2008-12-31")

# Create window for 2014
sp500_2014 <-window(sp500_returns, start = "2014-01-01", end = "2014-12-31")

# Plotting settings
par(mfrow = c(1, 2) , mar=c(3, 2, 2, 2))
names(sp500_2008) <- "sp500_2008"
names(sp500_2014) <- "sp500_2014"

# Plot histogram of 2008
chart.Histogram(sp500_2008, methods = c("add.density", "add.normal"))

# Plot histogram of 2014
chart.Histogram(sp500_2014, methods = c("add.density", "add.normal"))

# Calculate the SemiDeviation
SemiDeviation(sp500_monthly)

# Calculate the value at risk
VaR(sp500_monthly, p=0.05)
VaR(sp500_monthly, p=0.025)

# Calculate the expected shortfall
ES(sp500_monthly, p=0.05)
ES(sp500_monthly, p=0.025)

# Table of drawdowns
table.Drawdowns(sp500_monthly)

# Plot of drawdowns
chart.Drawdown(sp500_monthly)

# Create a grid
grid <- seq(from = 0, to = 1, by = 0.01)

# Initialize an empty vector for Sharpe ratios
vsharpe <- rep(NA, times = length(grid) )

# Create a for loop to calculate Sharpe ratios
for(i in 1:length(grid)) {
	weight <- grid[i]
	preturns <- weight * returns_equities + (1 - weight) * returns_bonds
	vsharpe[i] <- SharpeRatio.annualized(preturns)
}

# Plot weights and Sharpe ratio
plot(grid, vsharpe, xlab = "Weights", ylab= "Ann. Sharpe ratio")
abline(v = grid[vsharpe == max(vsharpe)], lty = 3)

# Create a scatter plot
chart.Scatter(returns_bonds, returns_equities, xlab = "bond returns", ylab = "equity returns", main = "bond-equity returns")

# Find the correlation
cor(returns_bonds, returns_equities)


# Merge returns_bonds and returns_equities
returns <- merge(returns_bonds, returns_equities)

# Find and visualize the correlation using chart.Correlation
chart.Correlation(returns)

# Visualize the rolling estimates using chart.RollingCorrelation
chart.RollingCorrelation(returns_bonds, returns_equities, width = 24)

# Create portfolio weights
weights <- c(0.40, 0.40, 0.10, 0.10)

# Create volatility budget
vol_budget <- StdDev(returns, portfolio_method = "component", weights = weights)
head(vol_budget)

# Make a table of weights and risk contribution
weights_percrisk <- cbind(weights, vol_budget$pct_contrib_StdDev)
colnames(weights_percrisk) <- c("weights", "perc vol contrib")

# Print the table
weights_percrisk

# Verify the class of returns
class(returns)

# Investigate the dimensions of returns
dim(returns)

# Create a vector of row means
ew_preturns <- rowMeans(returns)

# Cast the numeric vector back to an xts object
ew_preturns <- xts(ew_preturns, order.by = time(returns))

# Plot ew_preturns
plot(ew_preturns)

# Load tseries
library(tseries)

# Create an optimized portfolio of returns
opt <- portfolio.optim(returns)

# Create pf_weights
pf_weights <- opt$pw

# Assign asset names
names(pf_weights) <- colnames(returns)

# Select optimum weights opt_weights
opt_weights <- pf_weights[pf_weights >= 0.01]

# Bar plot of opt_weights
barplot(opt_weights)

# Print expected portfolio return and volatility
opt$pm
opt$ps

# Create portfolio with target return of average returns
pf_mean <- portfolio.optim(returns, pm = mean(returns))

# Create portfolio with target return 10% greater than average returns
pf_10plus <- portfolio.optim(returns, pm = 1.1 * mean(returns))

# Print the standard deviations of both portfolios
pf_mean$ps
pf_10plus$ps


# Calculate the proportion increase in standard deviation
(pf_10plus$ps - pf_mean$ps) / (pf_mean$ps)

# Create vectors of maximum weights
max_weights1 <- rep(1, ncol(returns))
max_weights2 <- rep(0.10, ncol(returns))
max_weights3 <- rep(0.05, ncol(returns))

# Create an optimum portfolio with max weights of 100%
opt1 <- portfolio.optim(returns, reshigh = max_weights1)

# Create an optimum portfolio with max weights of 10%
opt2 <- portfolio.optim(returns, reshigh = max_weights2)

# Create an optimum portfolio with max weights of 5%
opt3 <- portfolio.optim(returns, reshigh = max_weights3)

# Calculate how many assets have a weight that is greater than 1% for each portfolio
sum(opt1$pw > .01)
sum(opt2$pw > .01)
sum(opt3$pw > .01)

# Print portfolio volatilites
opt1$ps
opt2$ps
opt3$ps

# Calculate each stocks mean returns
stockmu <- colMeans(returns)

# Create a grid of target values
grid <- seq(0.01, max(stockmu), length.out = 50)

# Create empty vectors to store means and deviations
vpm <- vpsd <- rep(NA, length(grid))

# Create an empty matrix to store weights
mweights <- matrix(NA, 50, 30)

# Create your for loop
for(i in 1:length(grid)) {
  opt <- portfolio.optim(x = returns , pm = grid[i])
  vpm[i] <- opt$pm
  vpsd[i] <- opt$ps
  mweights[i, ] <- opt$pw
}

# Create weights_minvar as the portfolio with the least risk
weights_minvar <- mweights[vpsd == min(vpsd), ]

# Calculate the Sharpe ratio
vsr <- (vpm - 0.0075) / vpsd

# Create weights_max_sr as the portfolio with the maximum Sharpe ratio
weights_max_sr <- mweights[vsr == max(vsr)]

# Create bar plot of weights_minvar and weights_max_sr
par(mfrow = c(2, 1), mar = c(3, 2, 2, 1))
barplot(weights_minvar[weights_minvar > 0.01])
barplot(weights_max_sr[weights_max_sr > 0.01])

# Create returns_estim
returns_estim <- window(returns, start = "1991-01-01", end = "2003-12-31")

# Create returns_eval
returns_eval <- window(returns, start = "2004-01-01", end = "2015-12-31")

# Create vector of max weights
max_weights <- rep(0.10, ncol(returns))

# Create portfolio with estimation sample
pf_estim <- portfolio.optim(returns_estim, reshigh = max_weights)

# Create portfolio with evaluation sample
pf_eval <- portfolio.optim(returns_eval, reshigh = max_weights)

# Create a scatter plot with evaluation portfolio weights on the vertical axis
plot(x=pf_estim$pw, y=pf_eval$pw)
abline(a = 0, b = 1, lty = 3)

# Create returns_pf_estim
returns_pf_estim <- Return.portfolio(returns_estim, pf_estim$pw, rebalance_on = "months")

# Create returns_pf_eval
returns_pf_eval <- Return.portfolio(returns_eval, pf_estim$pw, rebalance_on = "months")

# Print a table for your estimation portfolio
table.AnnualizedReturns(returns_pf_estim)

# Print a table for your evaluation portfolio
 table.AnnualizedReturns(returns_pf_eval)

######################################
# Intermediate Portfolio Analysis
######################################
# Load the package
library(PortfolioAnalytics)

# Load the data
data(indexes)

# Subset the data
index_returns <- indexes[,1:4]

# Print the head of the data
head(index_returns)

# Create the portfolio specification
port_spec <- portfolio.spec(colnames(index_returns))

# Add a full investment constraint such that the weights sum to 1
port_spec <- add.constraint(portfolio = port_spec, type = "full_investment")

# Add a long only constraint such that the weight of an asset is between 0 and 1
port_spec <- add.constraint(portfolio = port_spec, type = "long_only")

# Add an objective to minimize portfolio standard deviation
port_spec <- add.objective(portfolio = port_spec, type = "risk", name = "StdDev")

# Solve the optimization problem
opt <- optimize.portfolio(index_returns, portfolio = port_spec, optimize_method = "ROI")

# Print the results of the optimization
print(opt)

# Extract the optimal weights
extractWeights(opt)

# Chart the optimal weights
chart.Weights(opt)

# Create the portfolio specification
port_spec <- portfolio.spec(assets = colnames(index_returns))

# Add a full investment constraint such that the weights sum to 1
port_spec <- add.constraint(portfolio = port_spec, type = "full_investment")

# Add a long only constraint such that the weight of an asset is between 0 and 1
port_spec <- add.constraint(portfolio = port_spec, type = "long_only")

# Add an objective to maximize portfolio mean return
port_spec <- add.objective(portfolio = port_spec, type = "return", name = "mean")

# Add an objective to minimize portfolio variance
port_spec <- add.objective(portfolio = port_spec, type = "risk", name = "var", risk_aversion = 10)

# Solve the optimization problem
opt <- optimize.portfolio(R = index_returns, portfolio = port_spec, optimize_method = "ROI")

# Get the column names of the returns data
asset_names <- colnames(asset_returns)

# Create a portfolio specification object using asset_names
port_spec <- portfolio.spec(asset_names)

# Get the class of the portfolio specification object
class(port_spec)

# Print the portfolio specification object
print(port_spec)

# Add the weight sum constraint
port_spec <- add.constraint(portfolio = port_spec, type = "weight_sum", min_sum = 1, max_sum = 1)

# Add the box constraint
port_spec <- add.constraint(portfolio = port_spec, type = "box", min = c(0.10,0.10,0.10,0.10,0.10, 0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05), max = 0.40)

# Add the group constraint
port_spec <- add.constraint(portfolio = port_spec, type = "group", groups = list(c(1, 5, 7, 9, 10, 11), c(2, 3, 4, 6, 8,12)), group_min = 0.40, group_max = 0.60)

# Print the portfolio specification object
print(port_spec)

# Add a return objective to maximize mean return
port_spec <- add.objective(portfolio = port_spec, type = "return", name = "mean")

# Add a risk objective to minimize portfolio standard deviation
port_spec <- add.objective(portfolio = port_spec, type = "risk", name = "StdDev")

# Add a risk budget objective
port_spec <- add.objective(portfolio = port_spec, type = "risk_budget", name = "StdDev", min_prisk = 0.05, max_prisk = 0.10)

# Print the portfolio specification object
print(port_spec)

# Run a single period optimization using random portfolios as the optimization method
opt <- optimize.portfolio(R = asset_returns, portfolio = port_spec, optimize_method = "random", rp = rp, trace = TRUE)

# Print the output of the single-period optimization
print(opt)

# Run the optimization backtest with quarterly rebalancing
opt_rebal <- optimize.portfolio.rebalancing(R = asset_returns, portfolio = port_spec, optimize_method = 'random', rp = rp, trace = TRUE, search_size = 1000, rebalance_on = 'quarters', training_period = 60, rolling_window = 60)

# Print the output of the optimization backtest
print(opt_rebal)

# Extract the objective measures for the single period optimization
extractObjectiveMeasures(opt)

# Extract the objective measures for the optimization backtest
extractObjectiveMeasures(opt_rebal)

# Extract the optimal weights for the single period optimization
extractWeights(opt)

# Chart the weights for the single period optimization
chart.Weights(opt)

# Extract the optimal weights for the optimization backtest
extractWeights(opt_rebal)

# Chart the weights for the optimization backtest
chart.Weights(opt_rebal)

# Add a return objective with "mean" as the objective name
port_spec <- add.objective(portfolio = port_spec, type = "return", name = "mean")

# Calculate the sample moments
moments <- set.portfolio.moments(R = asset_returns, portfolio = port_spec)

# Check if moments$mu is equal to the sample estimate of mean returns
moments$mu == colMeans(asset_returns)

# Add a risk objective with "StdDev" as the objective name
port_spec <- add.objective(portfolio = port_spec, type = "risk", name = "StdDev")

# Calculate the sample moments using set.portfolio.moments. Assign to a variable named moments.
moments <- set.portfolio.moments(R = asset_returns, portfolio = port_spec)

# Check if moments$sigma is equal to the sample estimate of the variance-covariance matrix
moments$sigma == cov(asset_returns)

# Print the portfolio specification object
print(port_spec)

# PortfolioAnalytics supports the "sample" method as well as three more advanced methods for estimating portfolio moments.
#
# "sample": Basic sample estimate of first four moments.
# "boudt": The first four moments are estimated by fitting a statistical factor model based on the work of Boudt et al., 2014.
# "black_litterman": The first two moments are estimated using the Black-Litterman framework.
# "Meucci": The first two moments are estimated using the Fully Flexible Views framework.

# Fit a statistical factor model to the asset returns
fit <- statistical.factor.model(R = asset_returns, k = 3)

# Estimate the portfolio moments using the "boudt" method with 3 factors
moments_boudt <- set.portfolio.moments(R = asset_returns, portfolio = port_spec, method = "boudt", k = 3)

# Check if the covariance matrix extracted from the model fit is equal to the estimate in `moments_boudt`
moments_boudt$sigma == extractCovariance(fit)

# The custom moment function should return a named list where the elements represent the moments:

# $mu: first moment (expected returns vector)
# $sigma: second moment (variance-covariance matrix)
# $m3: third moment (coskewness matrix)
# $m4: fourth moment (cokurtosis matrix)

# Define custom moment function
moments_robust <- function(R, portfolio){
  out <- list()
  out$mu <- cov.rob(R, method = 'mcd')$cov
  out
}

# Estimate the portfolio moments using the function you just defined
moments <- moments_robust(R = asset_returns, portfolio = port_spec)

# Check the moment estimate
cov.rob(asset_returns, method = 'mcd')$cov == moments$mu

# Run the optimization with custom moment estimates
opt_custom <- optimize.portfolio(R = asset_returns, portfolio = port_spec, optimize_method = "random", rp = rp, momentFUN = 'moments_robust')

# Print the results of the optimization with custom moment estimates
print(opt_custom)

# Run the optimization with sample moment estimates
opt_sample <- optimize.portfolio(R = asset_returns, portfolio = port_spec, optimize_method = "random", rp = rp)

# Print the results of the optimization with sample moment estimates
print(opt_sample)

# Custom annualized portfolio standard deviation
pasd <- function(R, weights, sigma, scale = 12){
  sqrt(as.numeric(t(weights) %*% sigma %*% weights)) * sqrt(scale)
}

# Add custom objective to portfolio specification
port_spec <- add.objective(portfolio = port_spec, type = "risk", name = "pasd")

# Print the portfolio specificaton object
print(port_spec)

# Run the optimization
opt <- optimize.portfolio(R = asset_returns, portfolio = port_spec, momentFUN = set_sigma, optimize_method = "random", rp = rp)

# Print the results of the optimization
print(opt)

# Load the package
library(PortfolioAnalytics)

# Load the data
data('edhec')

# Assign the data to a variable
asset_returns <- edhec

# Create a vector of equal weights
equal_weights <- rep(1 / ncol(asset_returns), ncol(asset_returns))

# Compute the benchmark returns
r_benchmark <- Return.portfolio(R = asset_returns, weights = equal_weights, rebalance_on = 'quarters')
colnames(r_benchmark) <- "benchmark"

# Plot the benchmark returns
plot(r_benchmark)


# Run the optimization
opt_rebal_base <- optimize.portfolio.rebalancing(R = asset_returns,
                                                 portfolio = port_spec,
                                                 optimize_method = "ROI",
                                                 rebalance_on = 'quarters',
                                                 training_period = 60,
                                                 rolling_window = 60)

# Print the results
print(opt_rebal_base)

# Chart the weights
chart.Weights(opt_rebal_base)

# Compute the portfolio returns
returns_base <- Return.portfolio(R = asset_returns, weights = extractWeights(opt_rebal_base))
colnames(returns_base) <- "base"


# Add a risk budget objective
port_spec <- add.objective(portfolio = port_spec,
                           type = 'risk_budget',
                           name = 'StdDev',
                           min_prisk = 0.05,
                           max_prisk = 0.10)

# Run the optimization
opt_rebal_rb <- optimize.portfolio.rebalancing(R = asset_returns,
                                               portfolio = port_spec,
                                               optimize_method = "random", rp = rp,
                                               trace = TRUE,
                                               rebalance_on = 'quarters',
                                               training_period = 60,
                                               rolling_window = 60)

# Chart the weights
chart.Weights(opt_rebal_rb)

# Chart the percentage contribution to risk
chart.RiskBudget(opt_rebal_rb, match.col = "StdDev", risk.type = 'percentage')

# Compute the portfolio returns
returns_rb <- Return.portfolio(R = asset_returns, weights = extractWeights(opt_rebal_rb))
colnames(returns_rb) <- "risk_budget"

# Run the optimization
opt_rebal_rb_robust <- optimize.portfolio.rebalancing(R = asset_returns,
                                                      momentFUN = 'moments_robust',
                                                      portfolio = port_spec,
                                                      optimize_method = "random", rp = rp,
                                                      trace = TRUE,
                                                      rebalance_on = 'quarters',
                                                      training_period = 60,
                                                      rolling_window = 60)

# Chart the weights
chart.Weights(opt_rebal_rb_robust)

# Chart the percentage contribution to risk
chart.RiskBudget(opt_rebal_rb_robust, match.col = "StdDev", risk.type = 'percentage')


# Compute the portfolio returns
returns_rb_robust <- Return.portfolio(R = asset_returns, weights = extractWeights(opt_rebal_rb_robust))
colnames(returns_rb_robust) <- "rb_robust"

# equal weight benchmark r_benchmark
# Minimize portfolio standard deviation with sample estimates (returns stored in returns_base).
# Minimize portfolio standard deviation with percentage contribution to risk using sample estimates (returns stored in returns_rb).
# Minimize portfolio standard deviation with percentage contribution to risk using robust estimates (returns stored in returns_rb_robust).

# Combine the returns
ret <- cbind(r_benchmark, returns_base, returns_rb, returns_rb_robust)

# Compute annualized returns
table.AnnualizedReturns(R = ret)

# Chart the performance summary
charts.PerformanceSummary(R = ret)

######################################
# Bond Valuation
######################################

# Create vector of cash flows
cf <- c(5,5,5,5,105)

# Convert to data frame
cf <- data.frame(cf)

# Add column t to cf
cf$t <- as.numeric(rownames(cf))

# Calculate pv_factor
cf$pv_factor <- 1 / (1 + 0.06)^cf$t

# Calculate pv
cf$pv <- cf$cf * cf$pv_factor

# Calculate the bond price
sum(cf$pv)

# Create function
bondprc <- function(p, r, ttm, y) {
  cf <- c(rep(p * r, ttm - 1), p * (1 + r))
  cf <- data.frame(cf)
  cf$t <- as.numeric(rownames(cf))
  cf$pv_factor <- 1 / (1 + y)^cf$t
  cf$pv <- cf$cf * cf$pv_factor
  sum(cf$pv)
}

# Load Quandl package
library(Quandl)

# Obtain Moody's Baa index data
baa <- Quandl("FED/RIMLPBAAR_N_M")

# Identify 9/30/16 yield
baa_yield <- subset(baa, baa$Date == "2016-09-30")

# Generate prc_yld
prc_yld <- seq(0.02, 0.40, 0.01)

# Convert prc_yld to data frame
prc_yld <- data.frame(prc_yld)

# Calculate bond price given different yields
for (i in 1:nrow(prc_yld)) {
     prc_yld$price[i] <- bondprc(100, 0.10, 20, prc_yld$prc_yld[i])
}

# Plot P/YTM relationship
plot(prc_yld,
     type = "l",
     col = "blue",
     main = "Price/YTM Relationship")
# Load quantmod package
library(quantmod)

# Obtain Treasury yield data
t10yr <- getSymbols(Symbols = "DGS10", src = "FRED", auto.assign = FALSE)

# Subset data
t10yr <- t10yr['2006-01/2016-09']

# Plot yields
plot(x = index(t10yr),
     y = t10yr$DGS10,
     xlab = "Date",
     ylab = "Yield (%)",
     type = "l",
     col = "red",
     main = "10-Year US Treasury Yields")

# Examine first and last six elements in spread
head(spread)
tail(spread)

# Calculate spread$diff
spread$diff <- (spread$baa - spread$aaa) * 100

# Plot spread
plot(x = spread$date,
     y = spread$diff,
     type = "l",
     xlab = "Date",
     ylab = "Spread (bps)",
     col = "red",
     main = "Baa - Aaa Spread")

# Create cash flow vector
cf <- c(-95.79, 5, 5, 5, 5, 105)

# Create bond valuation function
bval <- function(i, cf,
     t=seq(along = cf))
     sum(cf / (1 + i)^t)

# Create ytm() function using uniroot
ytm <- function(cf) {
    uniroot(bval, c(0, 1), cf = cf)$root
}

# Use ytm() function to find yield
ytm(cf)

# Calculate the PV01
abs(bondprc(p = 100, r = 0.10, ttm = 20, y = 0.1001)
  - bondprc(p = 100, r = 0.10, ttm = 20, y = 0.10))

# Without a coupon to adjust for, the duration would equal the regular maturity

# Calculate bond price today
px <- bondprc(p = 100, r = 0.1, ttm = 20, y = 0.1)

# Calculate bond price if yields increase by 1%
px_up <- bondprc(p = 100, r = 0.1, ttm = 20, y = 0.11)

# Calculate bond price if yields decrease by 1%
px_down <- bondprc(p = 100, r = 0.1, ttm = 20, y = 0.09)

# Calculate approximate duration
duration <- (px_down - px_up) / (2 * px * 0.01)

# Estimate percentage change
duration_pct_change <- -8.545937 * -0.01

# Estimate dollar change
duration_dollar_change <- duration_pct_change*100

# Calculate approximate convexity
convexity <- (px_up + px_down - 2 * px) / (px * (0.01)^2)

# Estimate percentage change
convexity_pct_change <- 0.5 * convexity * (0.01)^2

# Estimate dollar change
convexity_dollar_change <- convexity_pct_change * 100

# Estimate change in price
price_change <- duration_dollar_change + convexity_dollar_change

# Estimate price
price <- px + price_change

# Load Quandl package
library(Quandl)

# Obtain Moody's Aaa yield
aaa <- Quandl("FED/RIMLPAAAR_N_M")

# identify yield on September 30, 2016
aaa_yield <- subset(aaa, aaa$Date == "2016-09-30")

# Convert yield into decimals
aaa_yield <- as.numeric(aaa_yield$Value/100)

# Layout the bond's cash flows
cf <- c(3, 3, 3, 3, 3, 3, 3, 103)

# Convert to data.frame
cf <- data.frame(cf)

# Add time indicator
cf$t <- seq(1,8,1)

# Calculate PV factor
cf$pv_factor <- 1 / (1 + aaa_yield)^cf$t

# Calculate PV
cf$pv <- cf$cf * cf$pv_factor

# Price bond
sum(cf$pv)

# Code cash flow function
alt_cf <- function(r, p, ttm) {
  c(rep(p * r, ttm - 1), p * (1 + r))
}

# Generate cf vector
alt_cf(r = 0.03, p = 100, ttm = 8)

######################################
# Credit Risk Modeling
######################################

# View the structure of loan_data
str(loan_data)

# Load the gmodels package
library(gmodels)

# Call CrossTable() on loan_status
CrossTable(loan_data$loan_status)

# Call CrossTable() on grade and loan_status
CrossTable(x=loan_data$grade, y=loan_data$loan_status, prop.r=TRUE,prop.c=FALSE, prop.t=FALSE, prop.chisq=FALSE)

# Create histogram of loan_amnt: hist_1
hist_1 <- hist(loan_data$loan_amnt)

# Print locations of the breaks in hist_1
hist_1$breaks

# Change number of breaks and add labels: hist_2
hist_2 <- hist(loan_data$loan_amnt, breaks = 200, xlab = "Loan amount",
               main = "Histogram of the loan amount")

# Plot the age variable
plot(loan_data$age, ylab="Age")

# Save the outlier's index to index_highage
index_highage <- which(loan_data$age > 122)

# Create data set new_data with outlier deleted
new_data <- loan_data[-index_highage, ]

# Make bivariate scatterplot of age and annual income
plot(loan_data$age, loan_data$annual_inc, xlab = "Age", ylab = "Annual Income")

# Look at summary of loan_data
summary(loan_data$int_rate)

# Get indices of missing interest rates: na_index
na_index <- which(is.na(loan_data$int_rate))

# Remove observations with missing interest rates: loan_data_delrow_na
loan_data_delrow_na <- loan_data[-c(na_index), ]

# Make copy of loan_data
loan_data_delcol_na <- loan_data

# Delete interest rate column from loan_data_delcol_na
loan_data_delcol_na$int_rate <- NULL

# Compute the median of int_rate
median_ir <- median(loan_data$int_rate, na.rm=TRUE)

# Make copy of loan_data
loan_data_replace <- loan_data

# Replace missing interest rates with median
loan_data_replace$int_rate[na_index] <- median_ir

# Check if the NAs are gone
summary(loan_data_replace$int_rate)

# Make the necessary replacements in the coarse classification example below
loan_data$ir_cat <- rep(NA, length(loan_data$int_rate))

loan_data$ir_cat[which(loan_data$int_rate <= 8)] <- "0-8"
loan_data$ir_cat[which(loan_data$int_rate > 8 & loan_data$int_rate <= 11)] <- "8-11"
loan_data$ir_cat[which(loan_data$int_rate > 11 & loan_data$int_rate <= 13.5)] <- "11-13.5"
loan_data$ir_cat[which(loan_data$int_rate > 13.5)] <- "13.5+"
loan_data$ir_cat[which(is.na(loan_data$int_rate))] <- "Missing"

loan_data$ir_cat <- as.factor(loan_data$ir_cat)

# Look at your new variable using plot()
plot(loan_data$ir_cat)

# Set seed of 567
set.seed(567)

# Store row numbers for training set: index_train
index_train <- sample(1:nrow(loan_data), 2/3 * nrow(loan_data))

# Create training set: training_set
training_set <- loan_data[index_train, ]

# Create test set: test_set
test_set <- loan_data[-index_train, ]

# Create confusion matrix
conf_matrix <- table(test_set$loan_status, model_pred)

tn <- conf_matrix[1,1]
fp <- conf_matrix[1,2]
fn <- conf_matrix[2,1]
tp <- conf_matrix[2,2]

# Compute classification accuracy
(tp + tn) / (tp + fp + tn + fn)

# Compute sensitivity
tp / (tp + fn)

# Build a glm model with variable ir_cat as a predictor
log_model_cat <- glm(loan_status ~ ir_cat , family= "binomial", data = training_set)

# Print the parameter estimates
log_model_cat

# Look at the different categories in ir_cat using table()
table(loan_data$ir_cat)

# Build the logistic regression model
log_model_multi <- glm(loan_status ~ age + ir_cat +grade + loan_amnt + annual_inc, family="binomial", data=training_set)

# Obtain significance levels using summary()
summary(log_model_multi)

# Build the logistic regression model
predictions_all_small <- predict(log_model_small, newdata = test_set, type = "response")

# Look at the range of the object "predictions_all_small"
range(predictions_all_small)

# Change the code below to construct a logistic regression model using all available predictors in the data set
log_model_small <- glm(loan_status ~ ., family = "binomial", data = training_set)

# Make PD-predictions for all test set elements using the the full logistic regression model
predictions_all_full <- predict(log_model_small, newdata=test_set, type="response")

# Look at the predictions range
range(predictions_all_full)

# The code for the logistic regression model and the predictions is given below
log_model_full <- glm(loan_status ~ ., family = "binomial", data = training_set)
predictions_all_full <- predict(log_model_full, newdata = test_set, type = "response")

# Make a binary predictions-vector using a cut-off of 15%
pred_cutoff_15 <- ifelse(predictions_all_full > 0.15, 1,0)

# Construct a confusion matrix
table(test_set$loan_status, pred_cutoff_15)

# Fit the logit, probit and cloglog-link logistic regression models
log_model_logit <- glm(loan_status ~ age + emp_cat + ir_cat + loan_amnt,
                       family = binomial(link = logit), data = training_set)
log_model_probit <- glm(loan_status ~ age + emp_cat + ir_cat + loan_amnt,
                       family = binomial(link = probit), data = training_set)

log_model_cloglog <-  glm(loan_status ~ age + emp_cat + ir_cat + loan_amnt,
                       family = binomial(link = cloglog), data = training_set)

# Make predictions for all models using the test set
predictions_logit <- predict(log_model_logit, newdata = test_set, type = "response")
predictions_probit <- predict(log_model_probit, newdata = test_set, type = "response")
predictions_cloglog <- predict(log_model_cloglog, newdata = test_set, type = "response")

# Use a cut-off of 14% to make binary predictions-vectors
cutoff <- 0.14
class_pred_logit <- ifelse(predictions_logit > cutoff, 1, 0)
class_pred_probit <- ifelse(predictions_probit > cutoff, 1, 0)
class_pred_cloglog <- ifelse(predictions_cloglog > cutoff, 1, 0)

# Make a confusion matrix for the three models
tab_class_logit <- table(true_val,class_pred_logit)
tab_class_probit <- table(true_val,class_pred_probit)
tab_class_cloglog <- table(true_val,class_pred_cloglog)

# Compute the classification accuracy for all three models
acc_logit <- sum(diag(tab_class_logit)) / nrow(test_set)
acc_probit <- sum(diag(tab_class_probit)) / nrow(test_set)
acc_cloglog <- sum(diag(tab_class_cloglog)) / nrow(test_set)

# Load package rpart in your workspace.
library(rpart)

# Change the code provided in the video such that a decision tree is constructed using the undersampled training set. Include rpart.control to relax the complexity parameter to 0.001.
tree_undersample <- rpart(loan_status ~ ., method = "class",
                          data = undersampled_training_set, control= rpart.control(cp=0.001))

# Plot the decision tree
plot(tree_undersample, uniform=TRUE)

# Add labels to the decision tree
text(tree_undersample)

# Change the code below such that a tree is constructed with adjusted prior probabilities.
tree_prior <- rpart(loan_status ~ ., method = "class", parms=list(prior=c(0.7,0.3)),
                    data = training_set, control=rpart.control(cp=0.001))

# Plot the decision tree
plot(tree_prior, uniform=TRUE)

# Add labels to the decision tree
text(tree_prior)

# Change the code below such that a decision tree is constructed using a loss matrix penalizing 10 times more heavily for misclassified defaults.
tree_loss_matrix <- rpart(loan_status ~ ., method = "class",
                          parms = list(loss = matrix(c(0, 10, 1, 0), ncol=2)),
                          control=rpart.control(cp=0.001),
                          data =  training_set)

# Plot the decision tree
plot(tree_loss_matrix, uniform=TRUE)

# Add labels to the decision tree
text(tree_loss_matrix)

# tree_prior is loaded in your workspace

# Plot the cross-validated error rate as a function of the complexity parameter
plotcp(tree_prior)

# Use printcp() to identify for which complexity parameter the cross-validated error rate is minimized.
printcp(tree_prior)

# Create an index for of the row with the minimum xerror
index <- which.min(tree_prior$cptable[ , "xerror"])

# Create tree_min
tree_min <- tree_prior$cptable[index, "CP"]

#  Prune the tree using tree_min
ptree_prior <- prune(tree_prior, cp = tree_min)

# Use prp() to plot the pruned tree
prp(ptree_prior)

# set a seed and run the code to construct the tree with the loss matrix again
set.seed(345)
tree_loss_matrix  <- rpart(loan_status ~ ., method = "class", data = training_set,
                           parms = list(loss=matrix(c(0, 10, 1, 0), ncol = 2)),
                           control = rpart.control(cp = 0.001))

# Plot the cross-validated error rate as a function of the complexity parameter
plotcp(tree_loss_matrix)

# Prune the tree using cp = 0.0012788
ptree_loss_matrix <- prune(tree_loss_matrix, cp=0.0012788)

# Use prp() and argument extra = 1 to plot the pruned tree
prp(ptree_loss_matrix, extra=1)

# set a seed and run the code to obtain a tree using weights, minsplit and minbucket
set.seed(345)
tree_weights <- rpart(loan_status ~ ., method = "class",
                      data = training_set,
                      weights= case_weights,
                      control = rpart.control(minsplit = 5, minbucket = 2, cp = 0.001))

# Plot the cross-validated error rate for a changing cp
plotcp(tree_weights)

# Create an index for of the row with the minimum xerror
index <- which.min(tree_weights$cp[ , "xerror"])

# Create tree_min
tree_min <- tree_weights$cp[index, "CP"]

# Prune the tree using tree_min
ptree_weights <- prune(tree_weights, cp=tree_min)

# Plot the pruned tree using the rpart.plot()-package
prp(ptree_weights, extra=1)

# Make predictions for each of the pruned trees using the test set.
pred_undersample <- predict(ptree_undersample, newdata = test_set,  type = "class")
pred_prior <- predict(ptree_prior, newdata = test_set, type = "class")
pred_loss_matrix <- predict(ptree_loss_matrix, newdata = test_set, type = "class")
pred_weights <- predict(ptree_weights, newdata = test_set, type = "class")

# Construct confusion matrices using the predictions.
confmat_undersample <- table(test_set$loan_status, pred_undersample)
confmat_prior <- table(test_set$loan_status, pred_prior)
confmat_loss_matrix <- table(test_set$loan_status, pred_loss_matrix)
confmat_weights <- table(test_set$loan_status, pred_weights)

# Compute the accuracies
acc_undersample <- sum(diag(confmat_undersample)) / nrow(test_set)
acc_prior <- sum(diag(confmat_prior)) / nrow(test_set)
acc_loss_matrix <- sum(diag(confmat_loss_matrix)) / nrow(test_set)
acc_weights <- sum(diag(confmat_weights)) / nrow(test_set)

# Make predictions for the probability of default using the pruned tree and the test set.
prob_default_prior <- predict(ptree_prior, newdata = test_set)[ ,2]

# Obtain the cutoff for acceptance rate 80%
cutoff_prior <- quantile(prob_default_prior, 0.80)

# Obtain the binary predictions.
bin_pred_prior_80 <- ifelse(prob_default_prior > cutoff_prior, 1, 0)

# Obtain the actual default status for the accepted loans
accepted_status_prior_80 <- test_set$loan_status[bin_pred_prior_80 == 0]

# Obtain the bad rate for the accepted loans
length(which(accepted_status_prior_80 == 1)) / length(accepted_status_prior_80)

# Have a look at the function strategy_bank
strategy_bank

# Apply the function strategy_bank to both predictions_cloglog and predictions_loss_matrix
strategy_cloglog <- strategy_bank(predictions_cloglog)
strategy_loss_matrix <- strategy_bank(predictions_loss_matrix)

# Obtain the strategy tables for both prediction-vectors
strategy_cloglog$table
strategy_loss_matrix$table

# Plot the strategy functions
par(mfrow = c(1,2))
plot(strategy_cloglog$accept_rate, strategy_cloglog$bad_rate,
     type = "l", xlab = "Acceptance rate", ylab = "Bad rate",
     lwd = 2, main = "logistic regression")

plot(strategy_loss_matrix$accept_rate, strategy_loss_matrix$bad_rate,
     type = "l", xlab = "Acceptance rate",
     ylab = "Bad rate", lwd = 2, main = "tree")

# Load the pROC-package
library(pROC)

# Construct the objects containing ROC-information
ROC_logit <- roc(test_set$loan_status, predictions_logit)
ROC_probit <- roc(test_set$loan_status, predictions_probit)
ROC_cloglog <- roc(test_set$loan_status, predictions_cloglog)
ROC_all_full <- roc(test_set$loan_status, predictions_all_full)

# Draw all ROCs on one plot
plot(ROC_logit)
lines(ROC_probit, col='blue')
lines(ROC_cloglog, col='red')
lines(ROC_all_full, col='green')

# Compute the AUCs
auc(ROC_logit)
auc(ROC_probit)
auc(ROC_cloglog)
auc(ROC_all_full)

# Construct the objects containing ROC-information
ROC_undersample <- roc(test_set$loan_status, predictions_undersample)
ROC_prior <- roc(test_set$loan_status, predictions_prior)
ROC_loss_matrix <- roc(test_set$loan_status, predictions_loss_matrix)
ROC_weights <- roc(test_set$loan_status, predictions_weights)

# Draw the ROC-curves in one plot
plot(ROC_undersample)
lines(ROC_prior, col='blue')
lines(ROC_loss_matrix, col='red')
lines(ROC_weights, col='green')

# Compute the AUCs
auc(ROC_undersample)
auc(ROC_prior)
auc(ROC_loss_matrix)
auc(ROC_weights)

# Build four models each time deleting one variable in log_3_remove_ir
log_4_remove_amnt <- glm(loan_status ~ grade + annual_inc + emp_cat, 
                        family = binomial, data = training_set) 
log_4_remove_grade <- glm(loan_status ~ annual_inc + emp_cat, 
                        family = binomial, data = training_set) 
log_4_remove_inc <- glm(loan_status ~ grade + emp_cat, 
                        family = binomial, data = training_set) 
log_4_remove_emp <- glm(loan_status ~ grade + annual_inc, 
                        family = binomial, data = training_set) 

# Make PD-predictions for each of the models
pred_4_remove_amnt <- predict(log_4_remove_amnt, newdata = test_set, type = "response")
pred_4_remove_grade <- predict(log_4_remove_grade, newdata = test_set, type = "response")
pred_4_remove_inc <- predict(log_4_remove_inc, newdata = test_set, type = "response")
pred_4_remove_emp <- predict(log_4_remove_emp, newdata = test_set, type = "response")

# Compute the AUCs
auc(test_set$loan_status, pred_4_remove_amnt)
auc(test_set$loan_status, pred_4_remove_grade)
auc(test_set$loan_status, pred_4_remove_inc)
auc(test_set$loan_status, pred_4_remove_emp)

# Build three models each time deleting one variable in log_4_remove_amnt
log_5_remove_grade <- glm(loan_status ~ annual_inc + emp_cat, family = binomial, data = training_set)
log_5_remove_inc <- glm(loan_status ~ grade  + emp_cat , family = binomial, data = training_set)
log_5_remove_emp <- glm(loan_status ~ grade + annual_inc, family = binomial, data = training_set)

# Make PD-predictions for each of the models
pred_5_remove_grade <- predict(log_5_remove_grade, newdata = test_set, type = "response")
pred_5_remove_inc <- predict(log_5_remove_inc, newdata = test_set, type = "response")
pred_5_remove_emp <- predict(log_5_remove_emp, newdata = test_set, type = "response")

# Compute the AUCs
auc(test_set$loan_status, pred_5_remove_grade)
auc(test_set$loan_status, pred_5_remove_inc)
auc(test_set$loan_status, pred_5_remove_emp)

# Plot the ROC-curve for the best model here
plot(roc(test_set$loan_status,pred_4_remove_amnt))

######################################
# Quantitative Risk Management
######################################

library(qrmdata)

# Load DJ index
data("DJ")

# Show head() and tail() of DJ index
head(DJ)
tail(DJ)

# Plot DJ index
plot(DJ)

# Extract 2008-2009 and assign to dj0809
dj0809 <- DJ['2008/2009']

# Plot dj0809
plot(dj0809)

# Load DJ constituents data
data("DJ_const")

# Apply names() and head() to DJ_const
names(DJ_const)
head(DJ_const)

# Extract AAPL and GS in 2008-09 and assign to stocks
# Another method:
#   data[index, colname]
#   data[index, c(col1index, col2index)]
stocks <- cbind(DJ_const$AAPL['2008/2009'], DJ_const$GS['2008/2009'])

# Plot stocks with plot.zoo()
plot.zoo(stocks)

# Load exchange rate data
data("GBP_USD")
data("EUR_USD")

# Plot the two exchange rates
plot(GBP_USD)
plot(EUR_USD)

# Plot a USD_GBP exchange rate
plot(1/GBP_USD)

# Merge the two exchange rates GBP_USD and EUR_USD
fx <- merge(GBP_USD, EUR_USD, all = TRUE)

# Extract 2010-15 data from fx and assign to fx0015
fx0015 <- fx['2010/2015']

# Plot the exchange rates in fx0015
plot.zoo(fx0015)

# Compute the log-returns of dj0809 and assign to dj0809_x
dj0809_x <- diff(log(dj0809))

# Plot the log-returns
plot(dj0809_x)

# Compute the log-returns of djstocks and assign to djstocks_x
djstocks_x <- diff(log(djstocks))

# Plot the two share returns
plot.zoo(djstocks_x)

# Compute the log-returns of GBP_USD and assign to erate_x
erate_x <- diff(log(GBP_USD))

# Plot the log-returns
plot(erate_x)

# Plot djstocks in four separate plots
plot.zoo(djstocks)

# Plot djstocks in one plot and add legend
plot.zoo(djstocks, plot.type="single", col=1:4)
legend(julian(x = as.Date("2009-01-01")), y = 70, legend = names(DJ_const)[1:4], fill = 1:4)

# Compute log-returns and assign to djstocks_x
djstocks_x <- diff(log(djstocks))

# Plot djstocks_x in four separate plots
plot.zoo(djstocks_x)

# Plot djstocks_x with vertical bars
plot.zoo(djstocks_x, type="h")

# Plot djx
plot(djx)

# Plot weekly log-returns of djx
plot(apply.weekly(djx, sum), plot.type="single", type="h")

# Plot monthly log-returns of djx
plot(apply.monthly(djx, sum), type="h")

# Plot djreturns
plot.zoo(djreturns)

# Plot monthly log-returns of djreturns
plot.zoo(apply.monthly(djreturns, colSums), type="h")

# Plot gold and oil prices
plot(gold)
plot(oil)

# Calculate daily log-returns
goldx <- diff(log(gold))
oilx <- diff(log(oil))

# Calculate monthly log-returns
goldx_m <- apply.monthly(goldx, sum)
oilx_m <- apply.monthly(oilx, sum)

# Merge goldx_m and oilx_m into coms
coms <- merge(goldx_m, oilx_m)

# Plot coms with vertical bars
plot.zoo(coms, type="h")

# Make a pairwise scatterplot of coms
pairs(as.zoo(coms))

# Compute log-returns as zcb_x and simple returns as zcb_x2
zcb_x <- diff(log(zcb))
zcb_x2 <- diff(zcb)

# Plot zcb_x for 1, 5 and 10-year maturities
plot.zoo(zcb_x[,yield_cols])

# Plot zcb_x2 for 1, 5 and 10-year maturities
plot.zoo(zcb_x2[,yield_cols])

# Plot the yield curve for the first day of zcb
plot(maturity, zcb[1,], ylim = range(zcb), type = "l", ylab = "yield (%)", col = "red")

# Add a line for the last day of zcb
lines(maturity, tail(zcb,1))

# Calculate average and standard deviation of djx
mu <- mean(djx)
sigma <- sd(djx)

# Plot histogram of djx
hist(djx, nclass = 20, probability = TRUE)

# Add the normal density as a red line to histogram
lines(djx, dnorm(djx, mean=mu, sd=sigma), col = 'red')

# Plot non-parametric KDE of djx
plot(density(djx))

# Add the normal density as red line to KDE
lines(djx, dnorm(djx, mean=mu, sd=sigma), col = 'red')

# Make a Q-Q plot of djx and add a red line
qqnorm(djx)
qqline(djx, col="red")

# Calculate the length of djx as n
n <- length(djx)

# Generate n standard normal variables, make a Q-Q plot, add a red line
x1 <- rnorm(n)
qqnorm(x1)
qqline(x1, col="red")

# Generate n Student t variables, make a Q-Q plot, add a red line
x2 <- rt(n, df = 4)
qqnorm(x2)
qqline(x2, col="red")

# Generate n standard uniform variables, make a Q-Q plot, add red line
x3 <- runif(n)
qqnorm(x3)
qqline(x3, col="red")

# Calculate skewness and kurtosis of djx
skewness(djx)
kurtosis(djx)

# Carry out a Jarque-Bera test for djx
jarque.test(djx)

# Calculate skewness and kurtosis of djreturns
s <- apply(djreturns, MARGIN=2, FUN=skewness)
k <- apply(djreturns, MARGIN=2, FUN=kurtosis)

# Plot k against s and add text labels to identify stocks
plot(s, k, type="n")
text(s, k, names(s), cex = 0.6)

# Carry out Jarque-Bera tests for each constituent in djreturns
apply(djreturns, 2, jarque.test)

# Calculate weekly and monthly log-returns from djx_d
djx_w <- apply.weekly(djx_d, colSums)
djx_m <- apply.monthly(djx_d, colSums)

# Calculate the p-value for each series in djx_d
apply(djx_d, 2, function(v){jarque.test(v)$p.value})

# Calculate the p-value for each series in djx_w
apply(djx_w, 2, function(v){jarque.test(v)$p.value})

# Calculate the p-value for each series in djx_m
apply(djx_m, 2, function(v){jarque.test(v)$p.value})

# Calculate a 21-day moving sum of djx
djx21 <- rollapplyr(djx, width = 21, FUN = sum)[-(1:20)]

# Calculate a 63-day moving sum of djx
djx63 <- rollapplyr(djx, width = 63, FUN = sum)[-(1:62)]

# Merge the three series and plot
djx2 <- merge(djx, djx21, djx63, all = FALSE)
plot.zoo(djx2)

# Compute the skewness and kurtosis for each series in djx2
apply(djx2, 2, kurtosis)
apply(djx2, 2, skewness)

# Conduct the Jarque-Bera test to each series in djx2
apply(djx2, 2, jarque.test)

# Fit a Student t distribution to djx
tfit <- fit.st(djx)

# Define tpars, nu, mu, and sigma
tpars <- tfit$par.ests
nu <- tpars[1]
mu <- tpars[2]
sigma <- tpars[3]

# Plot a histogram of djx
hist(djx, nclass = 20, probability = TRUE, ylim = range(0, 40))

# Compute the fitted t density at the values djx
yvals <- dt((djx - mu)/sigma, df = nu)/sigma

# Superimpose a red line to show the fitted t density
lines(djx, yvals, col = "red")

# Plot the daily log-return series in fx_d
plot.zoo(fx_d)

# Apply the Jarque-Bera test to each of the series in fx_d
apply(fx_d, 2, jarque.test)

# Plot the monthly log-return series in fx_m
plot.zoo(fx_m, type="h")

# Apply the Jarque-Bera test to each of the series in fx_m
apply(fx_m, 2, jarque.test)

# Fit a Student t distribution to each of the series in fx_m
apply(fx_m, 2, function(v){fit.st(v)$par.ests})

# Plot the interest-rate return series zcbx_m and zcbx2_m
plot.zoo(zcbx_m, type="h")
plot.zoo(zcbx2_m, type="h")

# Make Q-Q plots of the 3rd component series of zcbx_m and zcbx2_m
qqnorm(zcbx_m[,3])
qqnorm(zcbx2_m[,3])

# Compute the kurtosis of each series in zcbx_m and zcbx2_m
apply(zcbx_m, 2, kurtosis)
apply(zcbx2_m, 2, kurtosis)

# Conduct the Jarque-Bera test on each series in zcbx_m and zcbx2_m
apply(zcbx_m, 2, jarque.test)
apply(zcbx2_m, 2, jarque.test)

# Compute the length n of djx
n <- length(djx)

#  Generate a normal sample of size n with parameters given by npars
ndata <- rnorm(n)*npars[2] + npars[1]

# Generate a t-distributed sample of size n with paramaters given by tpars
tdata <- rt(n, df = tpars[1])*tpars[3] + tpars[2]

# Make ndata and tdata into xts objects
ndatax <- xts(ndata, time(djx))
tdatax <- xts(tdata, time(djx))

# Merge djx, ndatax, and tdatax and plot
alldata <- merge(djx, ndatax, tdatax)
plot.zoo(alldata, type="h", ylim = range(alldata))

# Set up a plot region to show 3 plots at a time
par(mfrow = c(3, 1))

# Plot the acfs of djx, ndata and tdata
acf(djx)
acf(ndata)
acf(tdata)

# Plot the acfs of the absolute values
acf(abs(djx))
acf(abs(ndata))
acf(abs(tdata))

# Plot the acfs of the squares of the values
acf(djx^2)
acf(ndata^2)
acf(tdata^2)

# Apply the Ljung-Box test to djx
Box.test(djx, lag = 10, type = 'Ljung')

# Apply the Ljung-Box test to absolute values of djx
Box.test(abs(djx), lag = 10, type = 'Ljung')

# Apply the Ljung-Box test to all return series in djall
apply(djall, 2, Box.test, lag = 10, type = 'Ljung')

# Apply the Ljung-Box test to absolute values of all returns in djall
apply(abs(djall), 2, Box.test, lag = 10, type = 'Ljung')

# Create monthly log-returns from djx
djx_m <- apply.monthly(djx, sum)

# Apply Ljung-Box tests to raw and absolute values of djx_m
Box.test(djx_m, lag = 10, type = 'Ljung')
Box.test(abs(djx_m), lag = 10, type = 'Ljung')

# Create monthly log-returns from djall
djall_m <- apply.monthly(djall, colSums)

# Apply Ljung-Box tests to raw and absolute values of djall_m
apply(djall_m, 2, Box.test, lag = 10, type = 'Ljung')
apply(abs(djall_m), 2, Box.test, lag = 10, type = 'Ljung')

# Partition plotting area into 3 pieces
par(mfrow = c(1, 3))

# Plot djx_extremes
plot(djx_extremes, type="h")

# Compute the spaces between the times of the extremes
djx_spaces <- diff(time(djx_extremes))

# Make a histogram of these spaces
hist(as.numeric(djx_spaces))

# Make a Q-Q plot of djx_spaces against exp_quantiles
qqplot(exp_quantiles, djx_spaces)

# Carry out the previous 4 steps for iid_extremes
plot(iid_extremes, type="h")
iid_spaces <- diff(time(iid_extremes))
hist(as.numeric(iid_spaces))
qqplot(exp_quantiles, iid_spaces)

# Make a time series plot of indexes with plot.zoo and a pairwise scatterplot with pairs
plot.zoo(indexes)
pairs(as.zoo(indexes))

# Calculate the sample correlation matrix of indexes
cor(indexes)

# Plot the sample acfs and cross-correlation functions for the returns in indexes
acf(indexes)

# Plot the sample acfs and cross-correlations functions for the absolute values of indexes
cor(abs(indexes))
acf(abs(indexes))

# Plot fx and fx_w
plot.zoo(fx, type="h")
plot.zoo(fx_w, type="h")

# Make acf plots of fx and the absolute values of fx
acf(fx)
acf(abs(fx))

# Apply the Ljung-Box test to the components of fx and their absolute values
apply(fx, 2, Box.test, lag = 10, type = 'Ljung')
apply(abs(fx), 2, Box.test, lag = 10, type = 'Ljung')

# Make acf plots of fx_w and the absolute values of fx_w
acf(fx_w)
acf(abs(fx_w))

# Apply the Ljung-Box test to the components of fx_w and their absolute values
apply(fx_w, 2, Box.test, lag = 10, type = 'Ljung')
apply(abs(fx_w), 2, Box.test, lag = 10, type = 'Ljung')

# Make a sequence of 100 x-values going from -4*sigma to 4*sigma
xvals <- seq(from = -4*sigma, to = 4*sigma, length.out = 100)

# Compute the density of a N(mu, sigma^2) distribution at xvals
ndens <- dnorm(xvals, mean = mu, sd = sigma)

# Plot ndens against xvals
plot(xvals, ndens, type="l")

# Compute the 99% VaR and 99% ES of a N(mu, sigma^2) distribution
VaR99 <- qnorm(0.99, mean = mu, sd = sigma)
ES99 <- ESnorm(0.99, mu = mu, sd = sigma)

# Draw vertical lines at VaR99 and ES99 in red and green
abline(v = Var99, col = "red")
abline(v = ES99, col = "green")

# Plot the risk-factor data
plot.zoo(riskfactors)

# Calculate the log-returns, assign to returns, and plot
returns <- diff(log(riskfactors))[-1, ]
plot.zoo(returns)

# Use apply() to carry out the Jarque-Bera test for all 5 series
apply(returns, 2, jarque.test)

# Make a Q-Q plot against normal for the 5th return series and add a reference line
qqnorm(returns[, 5])
qqline(returns[, 5])

# Make a picture of the sample acfs for returns and their absolute values
acf(returns)
acf(abs(returns))

# Calculate the loss from a log-return of -0.1 for all risk factors
lossop(rep(-0.1, 5))

# Apply lossop() to returns and plot hslosses
hslosses <- lossop(returns)
plot(hslosses)

# Form a Q-Q plot of hslosses against normal
qqnorm(hslosses)

# Plot the sample acf of hslosses and their absolute values
acf(hslosses)
acf(abs(hslosses))

# Estimate the 99th sample percentile of the distribution of hslosses
quantile(hslosses, 0.99)

# Estimate the 99% ES
mean(hslosses[hslosses >= quantile(hslosses, 0.99)])

# Estimate the mean and standard deviation of hslosses
mu <- mean(hslosses)
sigma <- sd(hslosses)

# Compute the 99% quantile of a normal distribution
qnorm(0.99, mean=mu, sd=sigma)

# Compute the 99% ES of a normal distribution
ESnorm(0.99, mu=mu, sd=sigma)

# Set the interest rate r to be 0.01, the volatility sigma to be 0.2 and the strike K to be 100
r <- 0.01
sigma <- 0.2
K <- 100

# Look at the arguments of the Black_Scholes function
args(Black_Scholes)

# Price a European call option that matures in one year if the current stock price is 80
Black_Scholes(0, 80, r, sigma, K, 1, "call")

# Price a European call option that matures in one year if the current stock price is 120
Black_Scholes(0, 120, r, sigma, K, 1, "call")

# Price a European put option that matures in one year if the current stock price is 80
Black_Scholes(0, 80, r, sigma, K, 1,"put")

# Price a European put option that matures in one year if the current stock price is 120
Black_Scholes(0, 120, r, sigma, K, 1,"put")

# Plot the risk factors and the log-returns
plot.zoo(riskfactors)
plot.zoo(returns)

# Make a scatterplot of the two return series
plot(as.matrix(returns))

# Apply the Jarque-Bera test to the returns and make a Q-Q plot of the volatility log-returns
apply(returns, 2, jarque.test)
qqnorm(returns[,2])

# Create the sample acf of the returns and absolute returns
acf(returns)
acf(abs(returns))

# Calculate the correlation between the log-returns
cor(returns)

# Calculate the first loss
lossop(c(-0.1,-0.1), S = 80, sigma = 0.2)

# Calculate the second loss
lossop(c(-0.1,0.1), S = 100, sigma = 0.2)

# Create and plot hslosses
hslosses <- lossop(returns, S = 100, sigma = 0.2)
plot(hslosses)

# Form a Q-Q plot of hslosses against normal
qqnorm(hslosses)

# Plot the sample acf of raw data and absolute values in hslosses
acf(hslosses)
acf(abs(hslosses))

######################################
# Financial Trading in R
######################################
install.packages("remotes")
remotes::install_github("braverock/quantstrat")

