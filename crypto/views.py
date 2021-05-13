import time
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseNotFound
from PIL import Image
from .forms import TickerForm
from .tiingo import get_meta_data, get_price_data, get_graph, get_graph_mini
from .cpc import top100, metaData, priceData

# REDUCE VALUES FOR FASTER LOAD TIMES
MAX_REQUEST_LOGO = 10
MAX_REQUEST_GRAPH = 100

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            if metaData(ticker)['status']['error_code']!=400:
                return HttpResponseRedirect(ticker)
            else:
                context = {'ticker': ticker.upper()}
                return render(request, 'notFound.html', context)
    else:  
        form = TickerForm()

    response = top100()
    data = response['data']
    top100symbols = ''
    logoCount = 0
    graphCount = 0

    for coin in data:
        tid = coin['symbol']
        top100symbols += tid + 'usd'
        if logoCount<MAX_REQUEST_LOGO:
            coin['logo'] = metaData(tid)['data'][tid]['logo']
            logoCount += 1

        if graphCount<MAX_REQUEST_GRAPH:
            fig = get_graph_mini(tid)
            coin['chart'] = fig
            graphCount += 1
        coin['quote']['USD']['price'] = "{:,.2f}".format(float(coin['quote']['USD']['price']))
        if coin['quote']['USD']['percent_change_24h'] > 0:
            coin['color'] = 'text-success'
        else:
            coin['color'] = 'text-danger'

        coin['quote']['USD']['percent_change_24h'] = "{:,.2f}".format(coin['quote']['USD']['percent_change_24h'])
        
        if coin['quote']['USD']['market_cap'] >= 1000000000000:
            coin['quote']['USD']['market_cap'] = "{:.2f}".format(coin['quote']['USD']['market_cap']/1000000000000)+'T'
        elif coin['quote']['USD']['market_cap'] >= 1000000000:
            coin['quote']['USD']['market_cap'] = "{:.2f}".format(coin['quote']['USD']['market_cap']/1000000000)+'B'
        elif coin['quote']['USD']['market_cap'] >= 1000000:
            coin['quote']['USD']['market_cap'] = "{:.2f}".format(coin['quote']['USD']['market_cap']/1000000)+'M'
        elif coin['quote']['USD']['market_cap'] >= 1000:
            coin['quote']['USD']['market_cap'] = "{:.2f}".format(coin['quote']['USD']['market_cap']/1000)+'K'


        if coin['quote']['USD']['volume_24h'] >= 1000000000000:
            coin['quote']['USD']['volume_24h'] = str(int(coin['quote']['USD']['volume_24h']/1000000000000))+'T'
        elif coin['quote']['USD']['volume_24h'] >= 1000000000:
            coin['quote']['USD']['volume_24h'] = str(int(coin['quote']['USD']['volume_24h']/1000000000))+'B'
        elif coin['quote']['USD']['volume_24h'] >= 1000000:
            coin['quote']['USD']['volume_24h'] = str(int(coin['quote']['USD']['volume_24h']/1000000))+'M'
        elif coin['quote']['USD']['volume_24h'] >= 1000:
            coin['quote']['USD']['volume_24h'] = str(int(coin['quote']['USD']['volume_24h']/1000))+'K'
        else:
            coin['quote']['USD']['volume_24h'] = int(coin['quote']['USD']['volume_24h']/1000)
        
        coin['supply_usage'] = ''
        if coin['max_supply'] is None:
            coin['supply_usage_percentage'] = ''
            coin['max_supply'] = ''
        else:
            if float(coin['max_supply']) != 0:
                perc = float(coin['circulating_supply'])/float(coin['max_supply']) * 100
                coin['supply_usage_percentage'] = "{:.0f}".format(perc)+'%'
                if coin['max_supply'] >= 1000000000000:
                    coin['max_supply'] = '/ {:.2f}'.format(coin['max_supply']/1000000000000)+'T'
                elif coin['max_supply'] >= 1000000000:
                    coin['max_supply'] = '/ {:.2f}'.format(coin['max_supply']/1000000000)+'B'
                elif coin['max_supply'] >= 1000000:
                    coin['max_supply'] = '/ {:.2f}'.format(coin['max_supply']/1000000)+'M'
                elif coin['max_supply'] >= 1000:
                    coin['max_supply'] = '/ {:.2f}'.format(coin['max_supply']/1000)+'K'
                else:
                    coin['max_supply'] = '/ {:.2f}'.format(coin['max_supply']/1000)

        if coin['circulating_supply'] >= 1000000000000:
            coin['circulating_supply'] = "{:.2f}".format(coin['circulating_supply']/1000000000000)+'T'
        elif coin['circulating_supply'] >= 1000000000:
            coin['circulating_supply'] = "{:.2f}".format(coin['circulating_supply']/1000000000)+'B'
        elif coin['circulating_supply'] >= 1000000:
            coin['circulating_supply'] = "{:.2f}".format(coin['circulating_supply']/1000000)+'M'
        elif coin['circulating_supply'] >= 1000:
            coin['circulating_supply'] = "{:.2f}".format(coin['circulating_supply']/1000)+'K'
        else:
            coin['circulating_supply'] = "{:.2f}".format(coin['circulating_supply']/1000)
    context = {'form': form, 'data': data}
    return render(request, 'index.html', context)


def ticker(request, tid): 
    tid = tid.upper()
    fig = get_graph(tid)
    info = metaData(tid)
    context = {}
    context['ticker'] = tid
    context['meta'] = info['data'][tid]
    context['price'] = priceData(tid)['data'][tid]['quote']['USD']
    for key in context['price']:
        if key != 'last_updated':
            context['price'][key] = "{:.2f}".format(float(context['price'][key]))
        else:
            dateTime = context['price'][key].split('T')
            date = dateTime[0]
            time = dateTime[1]
            yyymmdd = date.split('-')
            date = yyymmdd[1] + '.' + yyymmdd[2] + '.' + yyymmdd[0]
            time = time.split('.')[0] + ' UTC'
            context['price'][key] = date + ' on ' + time
    context['fig'] = fig
    return render(request, 'ticker.html', context)

def error(request, tid):
    return render(request, 'notFound.html')