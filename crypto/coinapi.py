import requests
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#import pandas as pd

headers = {'X-CoinAPI-Key' : '7048DA48-DF2D-421A-8471-56A1FFFABA48'}

def historicalData(ticker='BTC'):
    url = 'https://rest.coinapi.io/v1/quotes/BITSTAMP_SPOT_BTC_USD/history?time_start=2021-04-09T00:00:00'
    response = requests.get(url, headers=headers).json()
    return response


if __name__ == '__main__':
    response = historicalData()
    formattedData = {}
    formattedData['ask_price'] = []
    formattedData['bid_price'] = []
    counter = []
    i = 0
    for data in response:
        counter.append(i)
        i+=1
        formattedData['ask_price'].append(data['ask_price']) 
        formattedData['bid_price'].append(data['bid_price'])
    print(formattedData['ask_price'])
    plt.style.use('fivethirtyeight')
    y_vals = [58094.26, 58091.35, 58091.35, 58099.46, 58099.41, 58099.46, 58100.0, 58100.0, 58100.0, 58106.22, 58126.1, 58126.1, 58134.57, 58135.2, 58135.2, 58137.0, 58136.96, 58136.91, 58136.96, 58128.57]
    x_vals = [i for i in range(len(y_vals))]
    plt.plot(counter, formattedData['ask_price'])
    # plt.plot(x_vals, y_vals)
    plt.show()
    # figure = go.Figure(
    #     data=[
    #         go.Candlestick(
    #             x = counter,
    #             low = formattedData['ask_price'],
    #             high = formattedData['bid_price'],
    #             close = formattedData['ask_price'],
    #             open = formattedData['bid_price'],
    #             increasing_line_color = 'green',
    #             decreasing_line_color = 'red'
    #         )
    #     ]
    # )
    # figure.show()