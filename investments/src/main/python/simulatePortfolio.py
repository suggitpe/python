#!/usr/bin/env python

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def simulate(startOfPeriod, endOfPeriod, stockSymbols, allocation):
    daysOfMarketOpen = getNyseDaysOfMarketOpenBetween(startOfPeriod, endOfPeriod)
    dataDictionaryOfCloseMarketData = getMarketCloseDataFor(stockSymbols, daysOfMarketOpen)    
    
    return outputCalculationsFromStats(startOfPeriod, endOfPeriod, stockSymbols, allocation, dataDictionaryOfCloseMarketData)
    #plotMarketDataFor(stockSymbols, daysOfMarketOpen, normalisedCloseData)

def getNyseDaysOfMarketOpenBetween(startOfPeriod, endOfPeriod):
   	timeOfDay = dt.timedelta(hours=16)
	return du.getNYSEdays(startOfPeriod, endOfPeriod, timeOfDay)

def getMarketCloseDataFor(aListOfSymbols, daysOfMarketOpen):
    #dataObject = da.DataAccess('Yahoo', cachestalltime=0)
    dataObject = da.DataAccess('Yahoo')

    rawMarketData = dataObject.get_data(daysOfMarketOpen, aListOfSymbols, createMarketKeys())
    dataDictionary = dict(zip(createMarketKeys(), rawMarketData))
    return dataDictionary['close']

def outputCalculationsFromStats(startOfPeriod, endOfPeriod, stockSymbols, allocation, dataDictionaryOfCloseMarketData):
	dailyReturns = calculateWeightedDailyReturnsFromCloseData(dataDictionaryOfCloseMarketData, allocation)

	averageOfAllocatedReturns = np.mean(dailyReturns)
	stdOfAllocatedReturns = np.std(dailyReturns)
	sharpeRatio = np.sqrt(250) * (averageOfAllocatedReturns / stdOfAllocatedReturns)
	cumulativeReturn = np.cumprod(dailyReturns + 1, axis=0)[-1]

	return [stdOfAllocatedReturns, averageOfAllocatedReturns, sharpeRatio, cumulativeReturn]

def calculateWeightedDailyReturnsFromCloseData(dataDictionaryOfCloseMarketData, allocation):
	normalisedCloseData = normalisePrices(dataDictionaryOfCloseMarketData)
	allocatedReturns = createWeightedPortfolioFrom(normalisedCloseData, allocation)
	tsu.returnize0(allocatedReturns)
	return allocatedReturns

def createWeightedPortfolioFrom(normalisedCloseData, allocation):
	return np.sum(normalisedCloseData * allocation, axis=1)

def createMarketKeys():
	#return ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	return ['close']

def plotMarketDataFor(stockSymbols, daysOfMarketOpen, normalisedCloseData):
    plt.clf()
    plt.plot(daysOfMarketOpen, normalisedCloseData)
    plt.legend(stockSymbols)
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    plt.savefig('foo.pdf', format='pdf')
    print("PDF chart created")

def normalisePrices(closingData):
    dataAsArray = closingData.values
    return dataAsArray / dataAsArray[0,:]

def proveAlgorythmWithKnownValuesTest():
	start = dt.datetime(2011, 1, 1)
	end = dt.datetime(2011, 12, 31)
	stocks = ['AAPL', 'GLD', 'GOOG', 'XOM']
	allocation = [0.4, 0.4, 0.0, 0.2]

	volatility, averageReturn, sharpeRatio, cumulativeReturn = simulate(start, end, stocks, allocation)

	print "Start Date: ", start
	print "End Date: ", end
	print "Stock symbols: ", stocks
	print "Optimal Allocation", allocation
	print "Sharpe ratio: ", sharpeRatio
	print "Volatility (STD): ", volatility
	print "Average Daily Return: ", averageReturn
	print "Cumulative Daily Return: ", cumulativeReturn

proveAlgorythmWithKnownValuesTest()
