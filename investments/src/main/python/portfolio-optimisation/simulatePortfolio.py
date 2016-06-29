#!/usr/bin/env python

import datetime as dt

import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import matplotlib.pyplot as plt
import numpy as np


def simulate(start_of_period, end_of_period, stock_symbols, allocation):
    days_of_market_open = get_nyse_days_of_market_open_between(start_of_period, end_of_period)
    data_dictionary_of_close_market_data = get_market_close_data_for(stock_symbols, days_of_market_open)

    return output_calculations_from_stats(allocation, data_dictionary_of_close_market_data)


# plotMarketDataFor(stockSymbols, daysOfMarketOpen, normalisedCloseData)


def get_nyse_days_of_market_open_between(start_of_period, end_of_period):
    time_of_day = dt.timedelta(hours=16)
    return du.getNYSEdays(start_of_period, end_of_period, time_of_day)


def get_market_close_data_for(list_of_symbols, days_of_market_open):
    # data_object = da.DataAccess('Yahoo', cachestalltime=0)
    data_object = da.DataAccess('Yahoo')

    raw_market_data = data_object.get_data(days_of_market_open, list_of_symbols, create_market_keys())
    data_dictionary = dict(zip(create_market_keys(), raw_market_data))
    return data_dictionary['close']


def output_calculations_from_stats(allocation, data_dictionary_of_close_market_data):
    daily_returns = calculate_weighted_daily_returns_from_close_data(data_dictionary_of_close_market_data, allocation)

    average_of_allocated_returns = np.mean(daily_returns)
    std_of_allocated_returns = np.std(daily_returns)
    sharpe_ratio = np.sqrt(250) * (average_of_allocated_returns / std_of_allocated_returns)
    cumulative_return = np.cumprod(daily_returns + 1, axis=0)[-1]

    return [std_of_allocated_returns, average_of_allocated_returns, sharpe_ratio, cumulative_return]


def calculate_weighted_daily_returns_from_close_data(data_dictionary_of_close_market_data, allocation):
    normalised_close_data = normalise_prices(data_dictionary_of_close_market_data)
    allocated_returns = create_weighted_portfolio_from(normalised_close_data, allocation)
    tsu.returnize0(allocated_returns)
    return allocated_returns


def create_weighted_portfolio_from(normalised_close_data, allocation):
    return np.sum(normalised_close_data * allocation, axis=1)


def create_market_keys():
    # return ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    return ['close']


def normalise_prices(closing_data):
    data_as_array = closing_data.values
    return data_as_array / data_as_array[0, :]


def prove_algorithm_with_known_values_test():
    start = dt.datetime(2011, 1, 1)
    end = dt.datetime(2011, 12, 31)
    stocks = ['AAPL', 'GLD', 'GOOG', 'XOM']
    allocation = [0.4, 0.4, 0.0, 0.2]

    volatility, average_return, sharpe_ratio, cumulative_return = simulate(start, end, stocks, allocation)

    print "Start Date: ", start
    print "End Date: ", end
    print "Stock symbols: ", stocks
    print "Optimal Allocation", allocation
    print "Sharpe ratio: ", sharpe_ratio
    print "Volatility (STD): ", volatility
    print "Average Daily Return: ", average_return
    print "Cumulative Daily Return: ", cumulative_return


def plot_market_data_for(stock_symbols, days_of_market_open, normalised_close_data):
    plt.clf()
    plt.plot(days_of_market_open, normalised_close_data)
    plt.legend(stock_symbols)
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    plt.savefig('foo.pdf', format='pdf')
    print("PDF chart created")


prove_algorithm_with_known_values_test()
