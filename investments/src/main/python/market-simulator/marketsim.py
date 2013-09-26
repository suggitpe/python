import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

import numpy as np
import datetime as dt

def simulateMarket(startingAmount, ordersToProcess, dailyReturnOutputFile):
	print "simulating market with starting amount of", startingAmount, "from", ordersToProcess
	rawOrders, stockSymbols, startDate, endDate = readOrdersFromInputFile(ordersToProcess)
	daysOfMarketOpen = getNyseDaysOfMarketOpenBetween(startDate, endDate)
	dataDictionaryOfCloseMarketData = getMarketCloseDataFor(stockSymbols, daysOfMarketOpen)

	print stockSymbols, startDate, endDate

def readOrdersFromInputFile(ordersToProcess):	
	rawData = np.genfromtxt(ordersToProcess, names="Year, Month, Day, Symbol, Direction, Amount", dtype='i4,i2,i2,S4,S4,i8', delimiter=',')
	data = np.sort(rawData, order=['Year','Month','Day'])
	symbols = getSymbolsFrom(data)
	startDate = dt.datetime(data[0]['Year'],data[0]['Month'],data[0]['Day'])
	endDate = dt.datetime(data[-1]['Year'],data[-1]['Month'],data[-1]['Day'])
	return [data, symbols, startDate, endDate]

def getSymbolsFrom(data):
	symbols = set()
	for row in data:
		symbols.add(row['Symbol'])
	return list(symbols)

def getNyseDaysOfMarketOpenBetween(startOfPeriod, endOfPeriod):
   	timeOfDay = dt.timedelta(hours=16)
	return du.getNYSEdays(startOfPeriod, endOfPeriod, timeOfDay)

def getMarketCloseDataFor(aListOfSymbols, daysOfMarketOpen):
    #dataObject = da.DataAccess('Yahoo', cachestalltime=0)
    dataObject = da.DataAccess('Yahoo')

    rawMarketData = dataObject.get_data(daysOfMarketOpen, aListOfSymbols, createMarketKeys())
    dataDictionary = dict(zip(createMarketKeys(), rawMarketData))
    return dataDictionary['close']

def createMarketKeys():
	#return ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	return ['close']

simulateMarket(10000, "orders.csv", "dailyPortfolioValue.csv")