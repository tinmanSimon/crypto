import coinbaseRequestUtils
import time

coinbaseMainDomain = "api.coinbase.com"
coinbaseExchangeDomain = "api.exchange.coinbase.com"

# this only gets the product ids that are ending with 'USD'.
def getProductsIDs():
    res = coinbaseRequestUtils.makeRequest('GET', coinbaseMainDomain, '/api/v3/brokerage/products')
    if res.status_code != 200: return []
    response = res.json()
    products = response['products']
    return [p['product_id'] for p in products if p['product_id'].split('-')[-1] == 'USD']

# by default if endUnixTime < 0, then it returns the latest 300 candles at the current moment.
# by default we request 1 hour candle stick data.
def getCandles(productId, granularity = 3600, endUnixTime = -1):
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
def sortProductsByVolatility():
    coinIDs = getProductsIDs()
    coinIDVolatilityTuples = []
    for coinID in coinIDs:
        print(f"Now dealing with {coinID}")
        candles = getCandles(coinID)
        if len(candles) < 2: 
            print(f"Error! candle ID: {coinID} has {len(candles)} items!")
            continue
        accumulatedDiffs = sum(abs(candle[4] - candle[3]) / candle[3] for candle in candles)
        coinIDVolatilityTuples.append((accumulatedDiffs, coinID))
    coinIDVolatilityTuples.sort(reverse=True)
    return coinIDVolatilityTuples


topVolatileCoins = sortProductsByVolatility()
print(topVolatileCoins)