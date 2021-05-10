import requests
import plotly
import plotly.graph_objects as go
import pandas as pd
from collections import defaultdict
import plotly.express as px
import datetime
from datetime import date, timedelta

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

# def get_graph(ticker):
#     url = "https://api.tiingo.com/tiingo/crypto/prices?tickers="+ticker.lower()+"usd&startDate=2019-04-29&resampleFreq=1440min"
#     response = requests.get(url, headers = headers)
#     tickerPrice = defaultdict(list)  
#     priceData = response.json()[0]['priceData']

#     for prices in priceData:
#         tickerPrice['open'].append(prices['open'])
#         tickerPrice['close'].append(prices['close'])
#         tickerPrice['high'].append(prices['high'])
#         tickerPrice['low'].append(prices['low'])
#         tickerPrice['date'].append(prices['date'].split('T')[0])

#     # print(tickerPrice)
#     # priceData = response.json()
#     # print(priceData)
#     fig  = go.Figure(data = [go.Candlestick(x=tickerPrice['date'],
#                                             open=tickerPrice['open'],
#                                             high=tickerPrice['high'],
#                                             low=tickerPrice['low'],
#                                             close=tickerPrice['close'],
#                                             increasing_line_color= 'rgb(49, 195, 166)',
#                                             )])
#     fig.update_layout(plot_bgcolor='rgb(52, 58, 64)', yaxis_title= ticker+' price in USD',)
#     graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
#     return graph_div

def get_graph(ticker):
    lastweek = date.today() - timedelta(days=1*365)
    lastweek = lastweek.strftime('%Y-%m-%d')
    url = "https://api.tiingo.com/tiingo/crypto/prices?tickers="+ticker.lower()+"usd&startDate="+lastweek+"&resampleFreq=1440min"
    response = requests.get(url, headers = headers)
    if response.json():
        tickerPrice = defaultdict(list)  
        priceData = response.json()[0]['priceData']
        for prices in priceData:
            prices['date'] = prices['date'].split('T')[0]
        hist = pd.DataFrame(priceData)
        hist = hist.set_index('date')
        hist.index = pd.to_datetime(hist.index)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                                x=hist.index, y = hist['close'],
                                mode='lines',
                                line = dict(width= 1.5, color='rgb(49, 195, 166)'),
                                stackgroup='one'
                                ))
        fig.update_layout(
                        title = dict(text =  ticker + ' Price Chart', font_size = 30, pad_t = 20, font_color = 'rgb(49, 195, 166)'),
                        font = dict(color = '#fffff9'), 
                        plot_bgcolor='rgb(52, 58, 64)', 
                        paper_bgcolor ='rgb(52, 58, 64)',
                        xaxis_title = None,
                        yaxis_title = 'Price in USD', 
                        xaxis = dict(showgrid = False,), 
                        yaxis = dict(showgrid = False),
                        margin=dict(l=0, r=0, t=0, b=0),
                        
                        )
        graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
        return graph_div
    else:
        return 'No historical data available'


def get_graph_mini(ticker):
    lastweek = date.today() - timedelta(days=7)
    lastweek = lastweek.strftime('%Y-%m-%d')
    url = "https://api.tiingo.com/tiingo/crypto/prices?tickers="+ticker.lower()+"usd&startDate="+lastweek+"&resampleFreq=1440min"
    response = requests.get(url, headers = headers)
    if response.json():
        tickerPrice = defaultdict(list)  
        priceData = response.json()[0]['priceData']
        for prices in priceData:
            prices['date'] = prices['date'].split('T')[0]

        hist = pd.DataFrame(priceData)
        hist = hist.set_index('date')
        hist.index = pd.to_datetime(hist.index)

        fig = go.Figure()
        if hist['close'][-1] > hist['close'][-2]:increasing = True
        else: increasing = False
        fig = go.Figure()
        if increasing:
            fig.add_trace(go.Scatter(
                                x=hist.index, y = hist['close'],
                                mode='lines',
                                line = dict(width= 1.5, color='rgb(49, 195, 166)'),
                                stackgroup='one'
                                ))
        else:
            fig.add_trace(go.Scatter(
                                x=hist.index, y = hist['close'],
                                mode='lines',
                                line = dict(width= 1.5, color='#f4282d'),
                                stackgroup='one'
                                ))
        fig.update_layout( 
                        plot_bgcolor='rgb(52, 58, 64)', 
                        paper_bgcolor ='rgb(52, 58, 64)',
                        xaxis_title = None,
                        yaxis_title = None, 
                        xaxis = dict(showgrid = False, color = 'rgb(52, 58, 64)'), 
                        yaxis = dict(showgrid = False),
                        width = 160,
                        height = 40,
                        margin=dict(l=0, r=0, t=0, b=0),
                        yaxis_visible=False,
                        xaxis_visible=False,
                        )
        graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
        return graph_div

# if __name__ == '__main__':
    