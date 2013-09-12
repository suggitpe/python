#!/usr/bin/env python

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tus
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

def readDataAndPlotDeltas():
    stockSymbols = ['AAPL', 'GLD', 'GOOG', '$SPX', 'XOM']
    startOfPeriod = dt.datetime(2010, 1, 1)
    endOfPeriod = dt.datetime(2010, 1, 31)
    readDataAndPlotDeltasFor(stockSymbols, startOfPeriod, endOfPeriod)

def readDataAndPlotDeltasFor(stockSymbols, startOfPeriod, endOfPeriod):
    daysOfMarketOpen = getNyseDaysOfMarketOpenBetween(startOfPeriod, endOfPeriod)
    plotMarketDataFor(stockSymbols, daysOfMarketOpen, getMarketCloseDataFor(stockSymbols, daysOfMarketOpen))

def getNyseDaysOfMarketOpenBetween(startOfPeriod, endOfPeriod):
   	timeOfDay = dt.timedelta(hours=16)
	return du.getNYSEdays(startOfPeriod, endOfPeriod, timeOfDay)

def getMarketCloseDataFor(aListOfSymbols, daysOfMarketOpen):
    dataObject = da.DataAccess('Yahoo')

    rawMarketData = dataObject.get_data(daysOfMarketOpen, aListOfSymbols, createMarketKeys())
    dataDictionary = dict(zip(createMarketKeys(), rawMarketData))
    return dataDictionary['close']

def createMarketKeys():
	return ['open', 'high', 'low', 'close', 'volume', 'actual_close']

def plotMarketDataFor(stockSymbols, daysOfMarketOpen, closingData):
    plt.clf()
    plt.plot(daysOfMarketOpen, normalisePrices(closingData))
    plt.legend(stockSymbols)
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    plt.savefig('foo.pdf', format='pdf')
    print("PDF chart created")

def normalisePrices(closingData):
    dataAsArray = closingData.values
    return dataAsArray / dataAsArray[0,:]

readDataAndPlotDeltas()