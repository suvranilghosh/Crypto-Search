import requests
import json
from PIL import Image 
import PIL 
import time

headers = {
    'X-CMC_PRO_API_KEY': 'ce2697eb-b5a1-43e3-800c-cfcc73debc90',
    'Accepts': 'application/json',
}
def top100():
    params = {'start': '1', 'limit': '100', 'convert': 'USD'}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    response = requests.get(url, params = params, headers = headers).json()
    return response

def metaData(ticker):
    params = {'symbol': ticker}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    response = requests.get(url, params = params, headers = headers).json()
    return response


# if __name__ == '__main__':
    # logo = Image.open("../AAVE.png")
    # logo.show()
    # data = top100()['data']
    # for coin in data:
    #     tid = coin['symbol']
    #     img_data = requests.get(metaData(tid)['data'][tid]['logo']).content
    #     with open(tid+'.png', 'wb') as handler:
    #         handler.write(img_data)
    #     time.sleep(3)