import requests
import json

headers = {
    'X-CMC_PRO_API_KEY': 'ce2697eb-b5a1-43e3-800c-cfcc73debc90',
    'Accepts': 'application/json',
}

def top100():
    params = {'start': '1', 'limit': '100', 'convert': 'USD'}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    response = requests.get(url, params = params, headers = headers).json()
    # print(response)
    return response

def metaData(ticker):
    params = {'symbol': ticker}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    response = requests.get(url, params = params, headers = headers).json()
    # print (response)
    return response

def priceData(ticker):
    params ={'symbol':ticker}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    response = requests.get(url, params = params, headers = headers).json()
    return response