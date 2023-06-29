
#Copyright (C) 2023 
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from django.http import HttpResponseRedirect


def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		if ticker :
			pk_name = "pk_f0325474eae44d6b8ee10f2c99aea53f"
			url = "https://api.iex.cloud/v1/data/core/quote/"+ ticker + "?token=" + pk_name
			api_request = requests.get(url)

			try:
				api = json.loads(api_request.content)

			except Exception as e :
				api = "Error..."

			context = {'title':'Home', 'api': api}
			return render(request, 'home.html', context) 
		else:
			context = {'title':'Home', 'ticker': "Enter a Ticker Symbol Above..."}
			return render(request, 'home.html', context) 

	else:
		context = {'title':'Home', 'ticker': "Enter a Ticker Symbol Above..."}
		return render(request, 'home.html', context) 


def about(request):
	context = {'first_name':'Ali', 'last_name': 'Juma', 'title':'About'}
	return render(request, 'about.html', context)

def add_stock(request):
	import requests
	import json
	pk_name = "pk_f0325474eae44d6b8ee10f2c99aea53f"

	if request.method == 'POST':
		form = StockForm(request.POST or None)
		ticker = request.POST['ticker']
		if form.is_valid():
			form.save()
			messages.success(request, "Stock Has Been Added")
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		apiArr = []
		for ticker_item in ticker :

			url = "https://api.iex.cloud/v1/data/core/quote/"+ str(ticker_item) + "?token=" + pk_name
			api_request = requests.get(url)
			try:
				api = json.loads(api_request.content)
				Obj = {}
				Obj['id'] = ticker_item.id
				Obj['companyName'] = api[0]['companyName']
				Obj['latestPrice'] = api[0]['latestPrice']
				Obj['previousClose'] = api[0]['previousClose']
				Obj['marketCap'] = str(api[0]['marketCap'])
				Obj['ytdChange'] = api[0]['ytdChange']
				Obj['week52High'] = api[0]['week52High']
				Obj['week52Low'] = api[0]['week52Low']
				apiArr.append(Obj)

			except Exception as e :
				api = "Error..."
		context = {'ticker':ticker, 'title':'Add Stock','apiArr':apiArr}
		return render(request, 'add_stock.html', context)

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, "Stock Has Been Deleted!!")
	return redirect('add_stock')


	#for our_unit in our_units:
	#    NameObj = {}
	#    NameObj['cpr'] = our_unit.cpr
	#    NameObj['Name'] = our_unit.name
	#    NameArray.append(NameObj)
