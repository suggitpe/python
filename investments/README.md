# Investments

## Common Metrics
 - Annual Return
    - (value[end]/value[start]) - 1
    - eg move from $100 to $110
    - (110/100) - 1 = 0.10 = 10%
 - Risk: STD of Daily Return
    - STD((value[i]/value[i-1]) - 1)
    - daily_returns[] = (value[i]/value[i-1]) -1
    - std = stdev(daily_returns)
 - Risk: Max Draw Down
    - the maximum drop over a period
 - Reward/Risk: Sharpe Ratio
    - Higher the better (return versus the risk)
    - Choose based on the higher ratio
    - sharpe = k * mean(daily_returns)/stdev(daily_returns)
    - where k = sqrt(250) ie the trading days in a year
 - Reward/Risk: Sortino Ratio
 - Jensen's Alpha
