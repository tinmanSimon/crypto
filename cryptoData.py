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

    # candleParams has the following attributes:
    # 'requestEndUnixTime' : -1, # the end time of request, by default it's the time now.
    # 'candleSize': 600 # the total number of candles for the requests. by default 600 cuz we might have HMA400
    # 'granularity' : 3600, # by default, granularity is 1 hour meaning 3600 seconds
    # 'product_id' : 'BTC-USD' # by default, using btc
    # returns a list of candles from coinbase.
    def getCandles(self, candleParams = {}):
        productId = candleParams.get('product_id', 'BTC-USD') 
        granularity = candleParams.get('granularity', 3600) 
        candleSize = candleParams.get('candleSize', 300) 
        endUnixTime = candleParams.get('endUnixTime', int(time.time()))  
        basePath = f"/products/{productId}/candles?granularity={granularity}"
        candles = []
        while candleSize > 0:
            startUnixTime = endUnixTime - granularity * min(candleSize, 300)
            path = basePath + f"&start={startUnixTime}&end={endUnixTime}"
            print(f"getCandles path : {path}")
            # currently coinbase main domain doesn't give candles, it should work but it doesn't. As tmp
            # workaround I use exchange domain for now.
            res = coinbaseRequestUtils.makeRequest('GET', coinbaseExchangeDomain, path)
            if res.status_code != 200: 
                print(f"Error! Failed to get coinbase candles for {path}")
                return []
            candles += res.json()
            candleSize -= 300
            endUnixTime = startUnixTime - 1
        return candles[::-1] # response is in reverse chronological, so we reverse it to chronological

    # returns a list of product IDs that are sorted in volatility's decreasing order.
    # I measure volatility using accumulated absolute open-close price differences ratio.
    # so accumulated abs(close price - open price) / open price.
    def sortProductsByVolatility(self, coinIDs):
        coinIDVolatilityTuples = []
        for coinID in coinIDs:
            print(f"Now dealing with {coinID}")
            candles = self.getCandles({'product_id' : coinID})
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

    # for candleParams, see for getCandles
    def drawCandles(self, candleParams = {}, drawParams={
        'HMAs' : [ # HMAs in the format of (window, color).
            (10, 'yellow'), 
            (20, 'green'), 
            (50, (8/255, 143/255, 143/255)), 
            (100, 'blue'), 
            (200, 'violet'), 
            (400, 'red')
        ], 
    }):
        df = pd.DataFrame(data=self.getCandles(candleParams), columns=self.coinbaseCandleColumns)
        df.set_index("Date", inplace=True)
        df.index = pd.to_datetime(df.index, unit='s')
        closeSeries = df["Close"]
        apds = [mpf.make_addplot(self.getHMA(closeSeries, window), color=color) for window, color in drawParams.get('HMAs', []) if window < closeSeries.size]
        mpf.plot(df, addplot=apds, volume=True,style='yahoo',type='candle')

    # expect series to be a pandas series
    def upTrend(self, series):
        return series.size > 1 and series.iat[-1] > series.iat[-2]
    
    def downTrend(self, series):
        return series.size > 1 and series.iat[-1] < series.iat[-2]
    
    # returns True if series1 golden crosses series2 in either of the last 2 candle sticks.
    # expect both series to have size > 2
    def goldenCross(self, series1, series2):
        if series1.size < 3 or series2.size < 3: return False
        crossOnCurCandle = series1.iat[-1] > series2.iat[-1] and series1.iat[-2] < series2.iat[-2]
        crossOnPrevCandle = series1.iat[-1] > series2.iat[-1] and series1.iat[-2] > series2.iat[-2] and series1.iat[-3] < series2.iat[-3]
        return crossOnCurCandle or crossOnPrevCandle
    
    # returns True if series1 dead crosses series2 in either of the last 2 candle sticks.
    # expect both series to have size > 2
    def deadCross(self, series1, series2):
        if series1.size < 3 or series2.size < 3: return False
        crossOnCurCandle = series1.iat[-1] < series2.iat[-1] and series1.iat[-2] > series2.iat[-2]
        crossOnPrevCandle = series1.iat[-1] < series2.iat[-1] and series1.iat[-2] < series2.iat[-2] and series1.iat[-3] > series2.iat[-3]
        return crossOnCurCandle or crossOnPrevCandle
    
    def determinTrends(self, closeSeries, productID, upTrendResults, downTrendResults):
        HMA50 = self.getHMA(closeSeries, 50)
        HMA100 = self.getHMA(closeSeries, 100)
        HMA10 = self.getHMA(closeSeries, 10)
        HMA20 = self.getHMA(closeSeries, 20)
        if self.upTrend(HMA50) and self.upTrend(HMA100):
            upTrendResults.append({'product_id' : productID})
            if self.goldenCross(HMA10, HMA20):
                upTrendResults.append({'product_id' : productID})
        if self.downTrend(HMA50) and self.downTrend(HMA100):
            downTrendResults.append({'product_id' : productID})
            if self.deadCross(HMA10, HMA20):
                downTrendResults.append({'product_id' : productID})

    def findSOS(self, df, productID, SOSs):
        opens, closes = df['Open'], df['Close']
        candleBodies = abs(closes - opens)
        for i in range(-2, -5, -1):
            averageSampleLen = 5
            maxBodies = max(candleBodies.iloc[(i - averageSampleLen):i])
            curBody = candleBodies.iloc[i]
            if curBody > (2 * maxBodies):
                SOSs.append({'product_id' : productID})
                print(f"{productID} at {i}")
                break

    # find trends over a list of products
    def findCurHourlyTrends(self, productIDs):
        downTrendProducts, upTrendProducts = [], []
        goldenCrossProducts, deadCrossProducts = [], []
        SOSs = []
        for productID in productIDs:
            print(f"Determine hourly trend for {productID}")
            candles = self.getCandles(candleParams={
                'granularity' : 3600,
                'product_id' : productID,
                'candleSize' : 300
            })
            dataFrame = pd.DataFrame(candles, columns=self.coinbaseCandleColumns)
            closeSeries = dataFrame['Close']
            self.determinTrends(closeSeries, productID, upTrendProducts, downTrendProducts)
            self.findSOS(dataFrame, productID, SOSs)
        return {
            'upTrendProducts' : upTrendProducts, 
            'downTrendProducts': downTrendProducts,
            'goldenCrossProducts': goldenCrossProducts,
            'deadCrossProducts' : deadCrossProducts,
            'SOSs' : SOSs
        }
    
    
