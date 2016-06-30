import unittest

class MarketDataTest(unittest.TestCase):
    def testGetMarketData(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
