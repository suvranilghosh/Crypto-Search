import requests
import plotly.graph_objects as go
import pandas as pd
from collections import defaultdict

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ea9bac3a674ad4d85b8ff86c3c794e444ba6bd41'
}

def get_meta_data(ticker):
    url = "https://api.tiingo.com/tiingo/crypto?tickers={}".format(ticker.lower())
    # print(ticker.lower())
    # url = "https://api.tiingo.com/tiingo/daily/{}".format(ticker)
    response = requests.get(url, headers=headers)
    meta = response.json()[0]
    return meta

def get_price_data(ticker):
    url = "https://api.tiingo.com/tiingo/crypto/prices?tickers={}".format(ticker.lower())
    # url = "https://api.tiingo.com/tiingo/daily/{}/prices".format(ticker)
    response = requests.get(url, headers = headers)
    # print(response.json()[0]['priceData'][0])
    priceData = response.json()[0]['priceData'][0]
    return priceData

def get_historical_price_data(ticker):
    return None

if __name__ == '__main__':
    url = "https://api.tiingo.com/tiingo/crypto/prices?tickers=btcusd&startDate=2019-04-29&resampleFreq=1440min"
    response = requests.get(url, headers = headers)
    tickerPrice = defaultdict(list)  
    priceData = response.json()[0]['priceData']

    for prices in priceData:
        tickerPrice['open'].append(prices['open'])
        tickerPrice['close'].append(prices['close'])
        tickerPrice['high'].append(prices['high'])
        tickerPrice['low'].append(prices['low'])
        tickerPrice['date'].append(prices['date'].split('T')[0])

    # print(tickerPrice)
    # priceData = response.json()
    # print(priceData)
    fig  = go.Figure(data = [go.Candlestick(x=tickerPrice['date'],
                                            open=tickerPrice['open'],
                                            high=tickerPrice['high'],
                                            low=tickerPrice['low'],
                                            close=tickerPrice['close'],
                                            color = 'cyan')])
    fig.show()