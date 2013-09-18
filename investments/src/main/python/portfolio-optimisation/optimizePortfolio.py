#!/usr/bin/env python

import simulatePortfolio as sim
import datetime as dt

def optimise(start, end, stocks):
	combinations = getAllocationCombinationsForFourStocks()
	bestSharp = 0.0
	bestAllocation = []
	for allocation in combinations:
		volatility, averageReturn, sharpeRatio, cumulativeReturn = sim.simulate(start, end, stocks, allocation)
		if sharpeRatio > bestSharp:
			bestSharp = sharpeRatio
			bestAllocation = allocation
	return bestAllocation

def getAllocationCombinationsForFourStocks():
	combinations = []
	for a in xrange(11):
		for b in xrange(11 - a):			
			for c in xrange(11-b):
				j = (a + b + c)
				if j < 11:
					combinations.append((a,b,c,10-j))
	return convertIntegerAllocationsToFloats(combinations)

def convertIntegerAllocationsToFloats(combinationsAsInts):
	floatCombinations = []
	for allocations in combinationsAsInts:
		floatCombinations.append([integerDigit/10.0 for integerDigit in allocations])
	return floatCombinations

def detailAllocation( start, end, stocks, allocation):
	volatility, averageReturn, sharpeRatio, cumulativeReturn = sim.simulate(start, end, stocks, allocation)

	print "###################################"
	print "Start Date: ", start
	print "End Date: ", end
	print "Stock symbols: ", stocks
	print "Optimal Allocation", allocation
	print "Sharpe ratio: ", sharpeRatio
	print "Volatility (STD): ", volatility
	print "Average Daily Return: ", averageReturn
	print "Cumulative Daily Return: ", cumulativeReturn
	print "###################################"

def main():
	start = dt.datetime(2011, 1, 1)
	end = dt.datetime(2011, 12, 31)
	stocks = ['C', 'GS', 'IBM', 'HNZ']
	#stocks = ['AAPL', 'GOOG', 'IBM', 'MKSF']
	detailAllocation(start, end, stocks, optimise(start, end, stocks))

main()

