#!/usr/bin/env python

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tus
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt


def readDataFromSources():
    stockSymbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    print stockSymbols

    startOfPeriod = dt.datetime(2010, 1, 1)
    endOfPeriod = dt.datetime(2010, 12, 31)

    marketData = getMarketCloseDataFor(stockSymbols, startOfPeriod, endOfPeriod)
    print marketData


def getMarketCloseDataFor(aListOfSymbols, aStartDate, aEndDate):
    timeOfDay = dt.timedelta(hours=16)
    daysOfMarketOpen = du.getNYSEdays(aStartDate, aEndDate, timeOfDay)

    dataObject = da.DataAccess('Yahoo')
    marketKeys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    marketData = dataObject.get_data(daysOfMarketOpen, aListOfSymbols, marketKeys)
    return marketData

readDataFromSources()