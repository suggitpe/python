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



def getDataFromMarket():
	startOfPeriod = dt.datetime(2008, 1, 1)
	endOfPeriod = dt.datetime(2009, 12, 31)
	daysOfMarketOpen = du.getNYSEdays(startOfPeriod, endOfPeriod, dt.timedelta(hours=16))
	dataObject = da.DataAccess('Yahoo')
	symbols = dataObject.get_symbols_from_list('sp5002012')
	symbols.append('SPY')
	rawMarketData = dataObject.get_data(daysOfMarketOpen, symbols, createMarketKeys)
	dataDictionary = dict(zip(createMarketKeys, rawMarketData))

def createMarketKeys():
	#return ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	return ['actual_close']

getDataFromMark