import unittest
import mock
import requests
import httpretty
import time

from BFXLight.client import Client

class BitfinexTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        time.sleep(0.5)


    def test_should_have_server(self):
        self.assertEqual("https://api.bitfinex.com/v1", self.client.server())


    def test_should_have_url_for_foo(self):
        expected = "https://api.bitfinex.com/v1/foo"
        self.assertEqual(expected, self.client.url_for("foo"))


    def test_should_have_url_for_path_arg(self):
        expected = "https://api.bitfinex.com/v1/foo/bar"
        actual = self.client.url_for('foo/%s', path_arg="bar")
        self.assertEqual(expected, actual)


    def test_should_have_url_with_parameters(self):
        expected = "https://api.bitfinex.com/v1/foo?a=1&b=2"
        actual = self.client.url_for('foo', parameters={'a': 1, 'b': 2})
        self.assertEqual(expected, actual)


    def test_should_have_url_for(self):
        expected = self.client.url_for("foo")
        self.assertEqual("https://api.bitfinex.com/v1/foo", expected)


    def test_should_have_url_for_with_path_arg(self):
        expected = "https://api.bitfinex.com/v1/foo/bar"
        path = "foo/%s"
        self.assertEqual(expected, self.client.url_for(path, path_arg='bar'))
        self.assertEqual(expected, self.client.url_for(path, 'bar'))


    def test_should_have_url_for_with_parameters(self):
        expected = "https://api.bitfinex.com/v1/foo?a=1"
        self.assertEqual(expected, self.client.url_for("foo", parameters={'a': 1}))
        self.assertEqual(expected, self.client.url_for("foo", None, {'a': 1}))


    def test_should_have_url_for_with_path_arg_and_parameters(self):
        expected = "https://api.bitfinex.com/v1/foo/bar?a=1"
        path = "foo/%s"
        self.assertEqual(expected, self.client.url_for(path, path_arg='bar', parameters={'a': 1}))
        self.assertEqual(expected, self.client.url_for(path, 'bar', {'a': 1}))


    def test_symbols(self):
        data = self.client.symbols()
        symbols = ["btcusd","ltcusd","ltcbtc","ethusd","ethbtc","etcbtc","etcusd","bfxusd","bfxbtc","rrtusd",
                   "rrtbtc","zecusd","zecbtc","xmrusd","xmrbtc","dshusd","dshbtc","bccbtc","bcubtc","bccusd","bcuusd"]
        for s in symbols:
            self.assertIn(s, symbols)

    def test_ticker(self):
        data = self.client.ticker("zecusd")
        for k in ['mid','bid', 'ask', 'last_price', 'timestamp']:
            self.assertIn(k, data)

    def test_today(self):
        data = self.client.today('dshbtc')
        for k in ['low', 'high', 'volume']:
            self.assertIn(k, data)



    def test_stats(self):
        data = self.client.stats('btcusd')
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        self.assertIn('period', data[1])


    def test_lendbook_eth(self):
        data = self.client.lendbook('eth')
        self.assertIn('asks', data)
        self.assertIn('bids', data)

    def test_lendbook_with_parameters(self):
        parameters = {'limit_bids': 2, 'limit_asks': 0}
        data = self.client.lendbook('btc', parameters)
        self.assertIn('bids', data)
        self.assertEquals(len(data['bids']), 2)
        self.assertEquals(len(data['asks']), 0)


    def test_order_book(self):
        data = self.client.order_book('xmrusd')
        self.assertIn('bids', data)

    def test_order_book_with_parameters(self):
        parameters = {'limit_bids': 2, 'limit_asks': 0}
        data = self.client.order_book('btcusd', parameters)
        self.assertIn('bids', data)
        self.assertEquals(len(data['bids']), 2)
        self.assertEquals(len(data['asks']), 0)



