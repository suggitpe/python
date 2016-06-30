#!/usr/bin/env python

import datetime as dt

import simulatePortfolio as sim


def optimise(start, end, stocks):
    combinations = get_allocation_combinations_for_four_stocks()
    best_sharp = 0.0
    best_allocation = []
    for allocation in combinations:
        volatility, average_return, sharpe_ratio, cumulative_return = sim.simulate(start, end, stocks, allocation)
        if sharpe_ratio > best_sharp:
            best_sharp = sharpe_ratio
            best_allocation = allocation
    return best_allocation


def get_allocation_combinations_for_four_stocks():
    combinations = []
    for a in xrange(11):
        for b in xrange(11 - a):
            for c in xrange(11 - b):
                j = (a + b + c)
                if j < 11:
                    combinations.append((a, b, c, 10 - j))
    return convert_integer_allocations_to_floats(combinations)


def convert_integer_allocations_to_floats(combinations_as_ints):
    float_combinations = []
    for allocations in combinations_as_ints:
        float_combinations.append([integerDigit / 10.0 for integerDigit in allocations])
    return float_combinations


def detail_allocation(start, end, stocks, allocation):
    volatility, average_return, sharpe_ratio, cumulative_return = sim.simulate(start, end, stocks, allocation)

    print "###################################"
    print "Start Date: ", start
    print "End Date: ", end
    print "Stock symbols: ", stocks
    print "Optimal Allocation", allocation
    print "Sharpe ratio: ", sharpe_ratio
    print "Volatility (STD): ", volatility
    print "Average Daily Return: ", average_return
    print "Cumulative Daily Return: ", cumulative_return
    print "###################################"


def main():
    start = dt.datetime(2011, 1, 1)
    end = dt.datetime(2011, 12, 31)
    stocks = ['C', 'GS', 'IBM', 'HNZ']
    # stocks = ['AAPL', 'GOOG', 'IBM', 'MKSF']
    detail_allocation(start, end, stocks, optimise(start, end, stocks))


main()
