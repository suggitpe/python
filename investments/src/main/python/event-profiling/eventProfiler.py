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



def getDataFromMarket(startOfPeriod, endOfPeriod):
	daysOfMarketOpen = du.getNYSEdays(startOfPeriod, endOfPeriod, dt.timedelta(hours=16))
	dataObject = da.DataAccess('Yahoo')
	symbols = dataObject.get_symbols_from_list('sp5002012')
	symbols.append('SPY')
	keys = createMarketKeys()
	rawMarketData = dataObject.get_data(daysOfMarketOpen, symbols, keys)
	dataDictionary = dict(zip(keys, rawMarketData))
	return [symbols, dataDictionary]

def createMarketKeys():
	return ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	#return ['actual_close']

def findEventsFrom( symbols, dataDictionary):
	closeData = dataDictionary['close']
	theMarket = closeData['SPY']
	events = createDataFrameSameSizeAs(closeData)
	timestamps = closeData.index

	print "Finding events"
	for symbol in symbols:
		for day in range(1, len(timestamps)):
			symbolPriceToday = closeData[symbol].ix[timestamps[day]]
			marketPriceToday = theMarket.ix[timestamps[day]]
			symbolPriceYesterday = closeData[symbol].ix[timestamps[day-1]]
			marketPriceYesterday = theMarket.ix[timestamps[day-1]]
			symbolReturnToday = (symbolPriceToday / symbolPriceYesterday) -1
			marketReturnToday = (marketPriceToday / marketPriceYesterday) -1

			if symbolReturnToday <= -0.03 and marketReturnToday >= 0.02:
				events[symbol].ix[timestamps[day]] = 1

	return events

def createDataFrameSameSizeAs(exampleDataFrame):
	dataFrame = copy.deepcopy(exampleDataFrame)
	dataFrame = dataFrame * np.NAN
	return dataFrame

def createTheEventProfileFrom(events, dataDictionary):
	print "Profiling the event data"
	ep.eventprofiler(events, dataDictionary, i_lookback=20, i_lookforward=20,
		s_filename="eventStudy.pdf", b_market_neutral=True, b_errorbars=True, 
		s_market_sym='SPY')

def profilePeriod():
	startOfPeriod = dt.datetime(2008, 1, 1)
	endOfPeriod = dt.datetime(2009, 12, 31)
	symbols, dataDictionary = getDataFromMarket(startOfPeriod, endOfPeriod)
	events = findEventsFrom(symbols, dataDictionary)
	createTheEventProfileFrom(events, dataDictionary)

profilePeriod()
