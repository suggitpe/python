#!/usr/bin/env python

import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import csv


def getDataFromMarket(startOfPeriod, endOfPeriod, symbolsFrom):
	print "Getting data"
	daysOfMarketOpen = du.getNYSEdays(startOfPeriod, endOfPeriod, dt.timedelta(hours=16))
	dataObject = da.DataAccess('Yahoo')
	symbols = dataObject.get_symbols_from_list(symbolsFrom)
	symbols.append('SPY')
	keys = createMarketKeys()
	rawMarketData = dataObject.get_data(daysOfMarketOpen, symbols, keys)
	dataDictionary = dict(zip(keys, rawMarketData))
	cleanDictionaryOfNans(keys, dataDictionary)
	return [symbols, dataDictionary]

def createMarketKeys():
	return ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	#return ['actual_close']

def cleanDictionaryOfNans(keys, dataDictionary):
	for key in keys:
		dataDictionary[key] = dataDictionary[key].fillna(method='ffill')
		dataDictionary[key] = dataDictionary[key].fillna(method='bfill')
		dataDictionary[key] = dataDictionary[key].fillna(1.0)

def createOrdersFrom( symbols, dataDictionary, eventTrigger):
	closeData = dataDictionary['actual_close']
	theMarket = closeData['SPY']
	orders = []
	timestamps = closeData.index

	print "Finding events"
	
	for day in range(1, len(timestamps)):
		for symbol in symbols:	
			symbolPriceToday = closeData[symbol].ix[timestamps[day]]
			marketPriceToday = theMarket.ix[timestamps[day]]
			symbolPriceYesterday = closeData[symbol].ix[timestamps[day-1]]
			marketPriceYesterday = theMarket.ix[timestamps[day-1]]
			symbolReturnToday = (symbolPriceToday / symbolPriceYesterday) -1
			marketReturnToday = (marketPriceToday / marketPriceYesterday) -1

			if symbolPriceYesterday >= eventTrigger and symbolPriceToday < eventTrigger:
				sellDate = timestamps[day+5]
				if(day+5 > len(timestamps)):
					sellDate = timestamps[-1]

				orders.append(createOrderFor(symbol, timestamps[day], 'Buy'))
				orders.append(createOrderFor(symbol, sellDate, 'Sell'))

	return orders

def createOrderFor(symbol, date, direction):
	return [date.year, date.month, date.day, symbol, direction, 100]

def writeOrdersToCsv(orders):
	print "Writing orders to CSV"
	with open('orders.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',') 
		for order in orders:
			writer.writerow(order)


def profilePeriod():
	startOfPeriod = dt.datetime(2008, 1, 1)
	endOfPeriod = dt.datetime(2009, 12, 31)
	symbolsFrom = 'sp5002012'
	eventTrigger = 8.0
	symbols, dataDictionary = getDataFromMarket(startOfPeriod, endOfPeriod, symbolsFrom)
	orders = createOrdersFrom(symbols, dataDictionary, eventTrigger)
	writeOrdersToCsv(orders)

	print "Orders created"

profilePeriod()
