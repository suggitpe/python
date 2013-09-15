#!/usr/bin/env python

import simulatePortfolio as sim
import datetime as dt

def testSimpleCase():
	start = dt.datetime(2011, 1, 1)
	end = dt.datetime(2011, 12, 31)
	stocks = ['AAPL', 'GLD', 'GOOG', 'XOM']
	allocation = [0.4, 0.4, 0.0, 0.2]

	sim.simulate(start, end, stocks, allocation)

testSimpleCase()
