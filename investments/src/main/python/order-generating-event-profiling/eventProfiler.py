#!/usr/bin/env python

import csv
import datetime as dt

import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du


def get_data_from_market(start_of_period, end_of_period, symbols_from):
    print "Getting data"
    days_of_market_open = du.getNYSEdays(start_of_period, end_of_period, dt.timedelta(hours=16))
    data_object = da.DataAccess('Yahoo')
    symbols = data_object.get_symbols_from_list(symbols_from)
    symbols.append('SPY')
    keys = create_market_keys()
    raw_market_data = data_object.get_data(days_of_market_open, symbols, keys)
    data_dictionary = dict(zip(keys, raw_market_data))
    clean_dictionary_of_nans(keys, data_dictionary)
    return [symbols, data_dictionary]


def create_market_keys():
    return ['open', 'high', 'low', 'close', 'volume', 'actual_close']


# return ['actual_close']


def clean_dictionary_of_nans(keys, data_dictionary):
    for key in keys:
        data_dictionary[key] = data_dictionary[key].fillna(method='ffill')
        data_dictionary[key] = data_dictionary[key].fillna(method='bfill')
        data_dictionary[key] = data_dictionary[key].fillna(1.0)


def create_orders_from(symbols, data_dictionary, event_trigger):
    close_data = data_dictionary['actual_close']
    # the_market = close_data['SPY']
    orders = []
    timestamps = close_data.index

    print "Finding events"

    for day in range(1, len(timestamps)):
        for symbol in symbols:
            symbol_price_today = close_data[symbol].ix[timestamps[day]]
            market_price_today = the_market.ix[timestamps[day]]
            symbol_price_yesterday = close_data[symbol].ix[timestamps[day - 1]]
            market_price_yesterday = the_market.ix[timestamps[day - 1]]
            symbol_return_today = (symbol_price_today / symbol_price_yesterday) - 1
            market_return_today = (market_price_today / market_price_yesterday) - 1

            if symbol_price_yesterday >= event_trigger and symbol_price_today < event_trigger:
                sell_date = timestamps[day + 5]
                if day + 5 > len(timestamps):
                    sell_date = timestamps[-1]

                orders.append(create_order_for(symbol, timestamps[day], 'Buy'))
                orders.append(create_order_for(symbol, sell_date, 'Sell'))

    return orders


def create_order_for(symbol, date, direction):
    return [date.year, date.month, date.day, symbol, direction, 100]


def write_orders_to_csv(orders):
    print "Writing orders to CSV"
    with open('orders.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for order in orders:
            writer.writerow(order)


def profile_period():
    start_of_period = dt.datetime(2008, 1, 1)
    end_of_period = dt.datetime(2009, 12, 31)
    symbols_from = 'sp5002012'
    event_trigger = 8.0
    symbols, data_dictionary = get_data_from_market(start_of_period, end_of_period, symbols_from)
    orders = create_orders_from(symbols, data_dictionary, event_trigger)
    write_orders_to_csv(orders)

    print "Orders created"


profile_period()
