#############################################################
## A bunch of unorganized notes from my datacamp courses
## bcutrell13@gmail.com - March 2019
#############################################################

# some good resources ->
# https://rstudio-pubs-static.s3.amazonaws.com/78839_afca73ae18194eaf8f1b86d399dde969.html
# http://www.thertrader.com/

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
