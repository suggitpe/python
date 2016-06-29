#!/usr/bin/env python

import datetime as dt

import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import numpy as np
import pandas as pd


def analyse(inputValuesFile, benchmark):
    fundData = readOrdersFromInputFile(inputValuesFile)
    startDate = fundData.index[0]
    endDate = fundData.index[-1]
    benchmarkData = calculateBenchmarkDataFor(benchmark, startDate, endDate)
    outputStatisticsFor(fundData, benchmarkData)


def calculateBenchmarkDataFor(benchmarkSymbol, startDate, endDate):
    daysOfMarketOpen = getNyseDaysOfMarketOpenBetween(startDate, endDate)
    data = getMarketCloseDataFor({benchmarkSymbol}, daysOfMarketOpen)
    data = addAverageReturnsTo(data, benchmarkSymbol)
    return data


def addAverageReturnsTo(data, key):
    data['Return'] = 0.0
    days = data.index
    for day in range(0, len(days)):
        if day != 0:
            yesterday = data[key].ix[days[day - 1]]
            today = data[key].ix[days[day]]
            dailyReturn = (today / yesterday) - 1
            data['Return'].ix[days[day]] = dailyReturn
    return data


def getNyseDaysOfMarketOpenBetween(startOfPeriod, endOfPeriod):
    endPlusOne = endOfPeriod + dt.timedelta(days=1)
    timeOfDay = dt.timedelta(hours=16)
    return du.getNYSEdays(startOfPeriod, endPlusOne, timeOfDay)


def getMarketCloseDataFor(aListOfSymbols, daysOfMarketOpen):
    # dataObject = da.DataAccess('Yahoo', cachestalltime=0)
    dataObject = da.DataAccess('Yahoo')

    rawMarketData = dataObject.get_data(daysOfMarketOpen, aListOfSymbols, createMarketKeys())
    dataDictionary = dict(zip(createMarketKeys(), rawMarketData))
    return dataDictionary['close']


def createMarketKeys():
    # return ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    return ['close']


def readOrdersFromInputFile(inputValuesFile):
    rawData = np.genfromtxt(inputValuesFile, names="Year, Month, Day, Value",
                            dtype="i4,i2,i2,f", delimiter=',')
    rawData = np.sort(rawData, order=['Year', 'Month', 'Day'])
    data = createDataFrameFrom(rawData)
    data = addAverageReturnsTo(data, 0)
    return data


def outputStatisticsFor(fundData, benchmark):
    print len(fundData)
    startDate = fundData.index[0]
    endDate = fundData.index[-1]

    fundAverageReturn = np.mean(fundData['Return'])
    benchmarkAverageReturn = np.mean(benchmark['Return'])

    fundStdOfReturn = np.std(fundData['Return'])
    benchmarkStdOfReturn = np.std(benchmark['Return'])

    fundTotalReturn = (fundData[0].ix[-1] / fundData[0].ix[0])
    benchmarkTotalReturn = (benchmark['$SPX'].ix[-1] / benchmark['$SPX'].ix[0])

    fundSharpeRatio = np.sqrt(250) * (fundAverageReturn / fundStdOfReturn)
    benchmarkSharpeRatio = np.sqrt(250) * (benchmarkAverageReturn / benchmarkStdOfReturn)

    print "The final value of the portfolio is"
    print "Data range: ", startDate, "to", endDate
    print ""
    print "Sharpe ratio of Fund:", fundSharpeRatio
    print "Sharpe ratio of $SPX:", benchmarkSharpeRatio
    print ""
    print "Total return of Fund:", fundTotalReturn
    print "Total return of $SPX:", benchmarkTotalReturn
    print ""
    print "Standard deviation of Fund:", fundStdOfReturn
    print "Standard deviation of $SPX:", benchmarkStdOfReturn
    print
    print "Average Daily Return of Fund", fundAverageReturn
    print "Average Daily Return of $SPX", benchmarkAverageReturn


def createDataFrameFrom(data):
    dates = []
    values = []
    for tuple in data:
        dates.append(createDateFrom(tuple))
        values.append(tuple['Value'])

    return pd.DataFrame(values, index=dates)


def createDateFrom(tuple):
    return dt.datetime(tuple['Year'], tuple['Month'], tuple['Day'])


# analyse('values.csv', '$SPX')
# analyse('values2.csv', '$SPX')
analyse('values4.csv', '$SPX')
