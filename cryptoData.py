import coinbaseRequestUtils
import time
import pandas as pd
import mplfinance as mpf
import math

coinbaseMainDomain = "api.coinbase.com"
coinbaseExchangeDomain = "api.exchange.coinbase.com"

class cryptoData:
    def __init__(self, debugMode = False):
        self.debugMode = debugMode
        self.productIDsDebugLength = 5
        self.coinbaseCandleColumns = ["Date", "Low", "High", "Open", "Close", "Volume"]

    # this only gets the product ids that are ending with 'USD'.
    def getProductsIDs(self):
        res = coinbaseRequestUtils.makeRequest('GET', coinbaseMainDomain, '/api/v3/brokerage/products')
        if res.status_code != 200: return []
        response = res.json()
        products = response['products']
        productIds = [p['product_id'] for p in products if p['product_id'].split('-')[-1] == 'USD']
        if self.debugMode: return productIds[:self.productIDsDebugLength]
        return productIds

    # by default if endUnixTime < 0, then it returns the latest 300 candles at the current moment.
    # by default we request 1 hour candle stick data.
    def getCandles(self, productId, granularity = 3600, endUnixTime = -1):
        path = f"/products/{productId}/candles?granularity={granularity}"
        if endUnixTime > 0:
            startUnixTime = endUnixTime - granularity * 300
            path += f"&start={startUnixTime}&end={endUnixTime}"

        # currently coinbase main domain doesn't give candles, it should work but it doesn't. As tmp
        # workaround I use exchange domain for now.
        res = coinbaseRequestUtils.makeRequest('GET', coinbaseExchangeDomain, path)
        if res.status_code != 200: return []
        return res.json()

    # returns a list of product IDs that are sorted in volatility's decreasing order.
    # I measure volatility using accumulated absolute open-close price differences ratio.
    # so accumulated abs(close price - open price) / open price.
    def sortProductsByVolatility(self, coinIDs):
        coinIDVolatilityTuples = []
        for coinID in coinIDs:
            print(f"Now dealing with {coinID}")
            candles = self.getCandles(coinID)
            if len(candles) < 2: 
                print(f"Error! candle ID: {coinID} has {len(candles)} items!")
                continue
            accumulatedDiffs = sum(abs(candle[2] - candle[1]) / candle[3] for candle in candles)
            coinIDVolatilityTuples.append({
                'volatility' : accumulatedDiffs,
                'product_id' : coinID
            })
        coinIDVolatilityTuples.sort(reverse=True, key=lambda a: a['volatility'])
        return coinIDVolatilityTuples

    def getTopVolatileProducts(self, resultSize = 50):
        productIDs = self.getProductsIDs()
        return self.sortProductsByVolatility(productIDs)[:resultSize]
    
    def getEWMA(self, series, window):
        return series.ewm(span=window, min_periods=window).mean()
    
    def getHMA(self, series, window):
        newSeries = 2 * self.getEWMA(series, window // 2) - self.getEWMA(series, window)
        return self.getEWMA(newSeries, int(math.sqrt(window)))

    def drawCandles(self, product_id, granularity = 3600):
        df = pd.DataFrame(data=self.getCandles(product_id, granularity)[::-1], columns=self.coinbaseCandleColumns)
        df.set_index("Date", inplace=True)
        df.index = pd.to_datetime(df.index, unit='s')

        closeSeries = df["Close"]

        apds = [ 
            mpf.make_addplot(self.getHMA(closeSeries, 5), color='orange'),
            mpf.make_addplot(self.getHMA(closeSeries, 10), color='green'),
            mpf.make_addplot(self.getHMA(closeSeries, 25), color='blue'),
            mpf.make_addplot(self.getHMA(closeSeries, 50), color='red')
        ]
        mpf.plot(df,addplot=apds, volume=True,style='yahoo',type='candle')
