from cryptoData import cryptoData

cryptoDataHandler = cryptoData()
cryptoDataHandler.drawCandles(candleParams={
    'product_id' : 'OXT-USD'
})