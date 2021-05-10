import requests
import plotly
import plotly.graph_objects as go
import pandas as pd
from collections import defaultdict
import plotly.express as px
from sys import argv
from datetime import date, timedelta
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ea9bac3a674ad4d85b8ff86c3c794e444ba6bd41'
}

if __name__ == '__main__':
    ticker = argv[1]
    lastweek = date.today() - timedelta(days=7)
    lastweek = lastweek.strftime('%Y-%m-%d')
    # print()
    url = "https://api.tiingo.com/tiingo/crypto/prices?tickers="+ticker.lower()+"usd&startDate="+lastweek+"&resampleFreq=1440min"
    response = requests.get(url, headers = headers)
    # print(response)
    if response.json(): 
        tickerPrice = defaultdict(list)  
        priceData = response.json()[0]['priceData']
        for prices in priceData:
            prices['date'] = prices['date'].split('T')[0]

        hist = pd.DataFrame(priceData)
        hist = hist.set_index('date')
        hist.index = pd.to_datetime(hist.index)
        if hist['close'][-1] > hist['close'][-2]:increasing = True
        else: increasing = False
        fig = go.Figure()
        if increasing:
            fig.add_trace(go.Scatter(
                                x=hist.index, y = hist['close'],
                                mode='lines',
                                line = dict(width= 2.5, color='rgb(49, 195, 166)'),
                                stackgroup='one'
                                ))
        else:
            fig.add_trace(go.Scatter(
                                x=hist.index, y = hist['close'],
                                mode='lines',
                                line = dict(width= 2.5, color='#f4282d'),
                                stackgroup='one'
                                ))
        fig.update_layout( 
                        plot_bgcolor='rgb(52, 58, 64)', 
                        paper_bgcolor ='rgb(52, 58, 64)',
                        xaxis_title = None,
                        yaxis_title = None, 
                        xaxis = dict(showgrid = False, color = 'rgb(52, 58, 64)'), 
                        yaxis = dict(showgrid = False),
                        width = 1600,
                        height = 400,
                        margin=dict(l=1, r=1, t=1, b=1),
                        yaxis_visible=False,
                        xaxis_visible=False,
                        )
        graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
        
        fig.show()