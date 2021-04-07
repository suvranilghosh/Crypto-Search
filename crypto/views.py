from .forms import TickerForm
from .tiingo import get_meta_data, get_price_data
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:  
        form = TickerForm()
    return render(request, 'index.html', {'form': form})

def ticker(request, tid):
    context = {}
    context['ticker'] = tid
    context['meta'] = get_meta_data(tid)
    context['meta']['baseCurrency'] = context['meta']['baseCurrency'].upper()

    context['price'] = (get_price_data(tid))
    context['price']['open'] = "{:.2f}".format(float(context['price']['open']))
    context['price']['high'] = "{:.2f}".format(float(context['price']['high']))
    context['price']['low'] = "{:.2f}".format(float(context['price']['low']))
    context['price']['close'] = "{:.2f}".format(float(context['price']['close']))
    context['price']['tradesDone'] = "{:.0f}".format(int(context['price']['tradesDone']))
    context['price']['volumeNotional'] = "{:.2f}".format(float(context['price']['volumeNotional']))
    context['price']['volume'] = "{:.2f}".format(float(context['price']['volume']))   
    return render(request, 'ticker.html', context)

