import requests

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