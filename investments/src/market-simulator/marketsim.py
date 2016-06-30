import copy
import csv
import datetime as dt

import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import numpy as np


def simulateMarket(startingAmount, ordersToProcess, dailyReturnOutputFile):
    print "Simulating market with starting amount of", startingAmount, "from", ordersToProcess
    rawOrders, stockSymbols, startDate, endDate = readOrdersFromInputFile(ordersToProcess)
    print "Processing orders starting from ", startDate, "to", endDate
    daysOfMarketOpen = getNyseDaysOfMarketOpenBetween(startDate, endDate)
    dataDictionaryOfCloseMarketData = getMarketCloseDataFor(stockSymbols, daysOfMarketOpen)
    portfolio = createPortfolioFrom(rawOrders, stockSymbols, createDataFrameSameSizeAs(dataDictionaryOfCloseMarketData))
    portfolioValue = enrichPortfolioWithValues(portfolio, dataDictionaryOfCloseMarketData, rawOrders, startingAmount)
    writePortfolioToCsv(portfolioValue, dailyReturnOutputFile)


def writePortfolioToCsv(portfolio, dailyReturnOutputFile):
    days = portfolio.index
    values = np.sum(portfolio.values, axis=1)
    with open(dailyReturnOutputFile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for idx in range(0, len(days)):
            writer.writerow([days[idx].year, days[idx].month, days[idx].day, values[idx]])


def debugPortfolio(portfolio, days):
    for day in days:
        dayValue = portfolio.ix[day]
        print day, dayValue.values


def enrichPortfolioWithValues(portfolio, dataDictionaryOfCloseMarketData, orders, startingAmount):
    portfolioValue = dataDictionaryOfCloseMarketData * portfolio
    portfolioValue = addCashToportfolio(portfolioValue, dataDictionaryOfCloseMarketData, orders, startingAmount)

    return portfolioValue


def addCashToportfolio(portfolio, dataDictionaryOfCloseMarketData, orders, startingAmount):
    portfolio['Cash'] = 0
    for order in orders:
        orderDate = dt.datetime(order['Year'], order['Month'], order['Day'], 16)
        orderSymbol = order['Symbol']
        orderAmount = order['Amount']
        priceOnDay = dataDictionaryOfCloseMarketData[orderSymbol].ix[orderDate]
        valueOfOrder = priceOnDay * orderAmount
        print order
        currentDayValue = portfolio['Cash'].ix[orderDate]
        if (order['Direction'] == 'Buy'):
            portfolio['Cash'].ix[orderDate] = currentDayValue + (valueOfOrder * -1)
        else:
            portfolio['Cash'].ix[orderDate] = currentDayValue + valueOfOrder

    days = portfolio.index
    for day in range(0, len(days)):
        currentDayNumber = portfolio['Cash'].ix[days[day]]
        if day == 0:
            portfolio['Cash'].ix[days[day]] = startingAmount + currentDayNumber
        if (day > 0):
            yesterdayDayNumber = portfolio['Cash'].ix[days[day - 1]]
            portfolio['Cash'].ix[days[day]] = currentDayNumber + yesterdayDayNumber

    return portfolio


def readOrdersFromInputFile(ordersToProcess):
    rawData = np.genfromtxt(ordersToProcess, names="Year, Month, Day, Symbol, Direction, Amount",
                            dtype='i4,i2,i2,S4,S4,i8', delimiter=',')
    data = np.sort(rawData, order=['Year', 'Month', 'Day'])
    symbols = getSymbolsFrom(data)
    startDate = dt.datetime(data[0]['Year'], data[0]['Month'], data[0]['Day'])
    endDate = dt.datetime(data[-1]['Year'], data[-1]['Month'], data[-1]['Day'])
    return [data, symbols, startDate, endDate]


def getSymbolsFrom(data):
    symbols = set()
    for row in data:
        symbols.add(row['Symbol'])
    return list(symbols)


def debug(rawOrders):
    print "Order book:"
    for order in rawOrders:
        print order


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
    return ['close']


def createDataFrameSameSizeAs(exampleDataFrame):
    dataFrame = copy.deepcopy(exampleDataFrame)
    dataFrame = dataFrame * np.NAN
    dataFrame = dataFrame.fillna(0)
    return dataFrame


def createPortfolioFrom(rawOrders, symbols, portfolio):
    applyOrdersTo(portfolio, rawOrders)
    updateChangeOrderDataIntoCucultiveTotals(portfolio, symbols)
    return portfolio


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


def updateChangeOrderDataIntoCucultiveTotals(emptyDataframe, symbols):
    days = emptyDataframe.index
    for day in range(0, len(days)):
        for symbol in symbols:
            if (day > 0):
                yesterdayDayNumber = emptyDataframe[symbol].ix[days[day - 1]]
                currentDayNumber = emptyDataframe[symbol].ix[days[day]]
                emptyDataframe[symbol].ix[days[day]] = currentDayNumber + yesterdayDayNumber

# simulateMarket(1000000, "orders.csv", "values.csv")
# simulateMarket(1000000, "orders2.csv", "values2.csv")
# simulateMarket(1000000, "orders3.csv", "values3.csv")
