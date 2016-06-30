#!/usr/bin/env python

import copy
import datetime as dt

import QSTK.qstkstudy.EventProfiler as ep
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import numpy as np


def get_data_from_market(start_of_period, end_of_period, symbols_from):
    daysOfMarketOpen = du.getNYSEdays(start_of_period, end_of_period, dt.timedelta(hours=16))
    dataObject = da.DataAccess('Yahoo')
    symbols = dataObject.get_symbols_from_list(symbols_from)
    symbols.append('SPY')
    keys = create_market_keys()
    rawMarketData = dataObject.get_data(daysOfMarketOpen, symbols, keys)
    dataDictionary = dict(zip(keys, rawMarketData))
    clean_dictionary_of_nans(keys, dataDictionary)
    return [symbols, dataDictionary]


def create_market_keys():
    return ['open', 'high', 'low', 'close', 'volume', 'actual_close']


# return ['actual_close']

def clean_dictionary_of_nans(keys, dataDictionary):
    for key in keys:
        dataDictionary[key] = dataDictionary[key].fillna(method='ffill')
        dataDictionary[key] = dataDictionary[key].fillna(method='bfill')
        dataDictionary[key] = dataDictionary[key].fillna(1.0)


def find_events_from(symbols, dataDictionary, eventTrigger):
    closeData = dataDictionary['actual_close']
    theMarket = closeData['SPY']
    events = create_data_frame_same_size_as(closeData)
    timestamps = closeData.index

    print "Finding events"
    for symbol in symbols:
        for day in range(1, len(timestamps)):
            symbolPriceToday = closeData[symbol].ix[timestamps[day]]
            marketPriceToday = theMarket.ix[timestamps[day]]
            symbolPriceYesterday = closeData[symbol].ix[timestamps[day - 1]]
            marketPriceYesterday = theMarket.ix[timestamps[day - 1]]
            symbolReturnToday = (symbolPriceToday / symbolPriceYesterday) - 1
            marketReturnToday = (marketPriceToday / marketPriceYesterday) - 1

            if symbolPriceYesterday >= eventTrigger and symbolPriceToday < eventTrigger:
                events[symbol].ix[timestamps[day]] = 1

    return events


def create_data_frame_same_size_as(exampleDataFrame):
    dataFrame = copy.deepcopy(exampleDataFrame)
    dataFrame = dataFrame * np.NAN
    return dataFrame


def create_the_event_profile_from(events, dataDictionary):
    print "Profiling the event data"
    ep.eventprofiler(events, dataDictionary, i_lookback=20, i_lookforward=20,
                     s_filename="eventStudy.pdf", b_market_neutral=True, b_errorbars=True,
                     s_market_sym='SPY')


def profile_period():
    start_of_period = dt.datetime(2008, 1, 1)
    end_of_period = dt.datetime(2009, 12, 31)
    symbols_from = 'sp5002012'
    event_trigger = 6.0
    symbols, data_dictionary = get_data_from_market(start_of_period, end_of_period, symbols_from)
    events = find_events_from(symbols, data_dictionary, event_trigger)
    create_the_event_profile_from(events, data_dictionary)


profile_period()
