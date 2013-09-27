import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

import numpy as np
import datetime as dt
import copy

def simulateMarket(startingAmount, ordersToProcess, dailyReturnOutputFile):
	print "Simulating market with starting amount of", startingAmount, "from", ordersToProcess
	rawOrders, stockSymbols, startDate, endDate = readOrdersFromInputFile(ordersToProcess)
	print "Processing orders starting from ", startDate, "to", endDate
	debug(rawOrders)
	daysOfMarketOpen = getNyseDaysOfMarketOpenBetween(startDate, endDate)
	dataDictionaryOfCloseMarketData = getMarketCloseDataFor(stockSymbols, daysOfMarketOpen)
	portfolio = createPortfolioFrom(rawOrders, stockSymbols, createDataFrameSameSizeAs(dataDictionaryOfCloseMarketData))

	print stockSymbols, startDate, endDate

def createPortfolioFrom(rawOrders, symbols, emptyDataframe):
	print "creating"
	days = emptyDataframe.index
	applyOrdersTo(emptyDataframe, rawOrders)
	print emptyDataframe.values


	# for day in range(0, len(days)):
	# 	for symbol in symbols:
	# 		yesterdayDayNumber = emptyDataframe[symbol].ix[days[day-1]]
	# 		delta = findOrderNumberFor(rawOrders, days[day], symbol)
	# 		if(delta != 0):
	# 			print delta
	# 		emptyDataframe[symbol].ix[days[day]] = yesterdayDayNumber + delta
	# 		currentDayNumber = emptyDataframe[symbol].ix[days[day]]
			
			#print symbol, days[day], yesterdayDayNumber, currentDayNumber 

def applyOrdersTo(emptyDataframe, orders):
	for order in orders:
		dateOfOrder = dt.datetime(order['Year'], order['Month'], order['Day'], 16)
		symbol = order['Symbol']
		currentValue = emptyDataframe.loc[dateOfOrder][symbol]
		amountToAdd = applyBuySellTo(order['Amount'], order['Direction'])
		emptyDataframe.loc[dateOfOrder][symbol] = currentValue + amountToAdd

def applyBuySellTo(Amount, Direction):
	if Direction == 'Buy':
		return Amount
	else:
		return Amount * -1

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
	endPlusOne = endOfPeriod + dt.timedelta(days=1)
   	timeOfDay = dt.timedelta(hours=16)
	return du.getNYSEdays(startOfPeriod, endPlusOne, timeOfDay)

def getMarketCloseDataFor(aListOfSymbols, daysOfMarketOpen):
    #dataObject = da.DataAccess('Yahoo', cachestalltime=0)
    dataObject = da.DataAccess('Yahoo')

    rawMarketData = dataObject.get_data(daysOfMarketOpen, aListOfSymbols, createMarketKeys())
    dataDictionary = dict(zip(createMarketKeys(), rawMarketData))
    return dataDictionary['close']

def createMarketKeys():
	return ['close']

def debug(rawOrders):
	print "Order book:"
	for order in rawOrders:
		print order

def createDataFrameSameSizeAs(exampleDataFrame):
	dataFrame = copy.deepcopy(exampleDataFrame)
	dataFrame = dataFrame * np.NAN
	dataFrame = dataFrame.fillna(0)
	return dataFrame

simulateMarket(10000, "orders.csv", "dailyPortfolioValue.csv")