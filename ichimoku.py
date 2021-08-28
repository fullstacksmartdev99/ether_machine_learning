import numpy
import datetime
import time
import statistics
import pickle
from pandas.tseries.offsets import BDay
import requests

min_n = 25

def find_period_high(data):
	return(max(data))

def find_period_low(data):
	return(min(data))

#conversion line
def find_tenkan_sen(prices, tenkan_period):
	data = prices[-tenkan_period:]
	period_high = find_period_high(data)
	period_low = find_period_low(data)
	kenkan_sen = ((period_high) + ( period_low)) / 2
	return kenkan_sen

#base line
def find_kijun_sen(prices, tenkan_period):
	kijun_period = tenkan_period * 3
	data = prices[-kijun_period:]
	period_high = find_period_high(data)
	period_low = find_period_low(data)
	kijun_sen = ((period_high) + (period_low)) / 2
	return kijun_sen

#leading span a
def find_senkou_a(prices, tenkan_period):
	prices = prices[:-26]
	tenkan_sen = find_tenkan_sen(prices, tenkan_period)
	kijun_sen = find_kijun_sen(prices,tenkan_period)
	senkou_a = (tenkan_sen + kijun_sen) / 2
	return senkou_a

#leading span b
def find_senkou_b(prices, tenkan_period):
	kijun_period = tenkan_period * 3
	prices = prices[:-26]
	data = prices[-kijun_period * 2:]
	period_high = find_period_high(data)
	period_low = find_period_low(data)
	senkou_b = (period_high + period_low) / 2
	return senkou_b

###gets ICHIMOKU
def find_sentiment(prices,tenkan_period):
	current_price = prices[-1]
	tenkan_sen = find_tenkan_sen(prices, tenkan_period)
	kijun_sen = find_kijun_sen(prices,tenkan_period)
	senkou_a = find_senkou_a(prices,tenkan_period)
	senkou_b = find_senkou_b(prices,tenkan_period)

	cloud_color = 'green'
	if senkou_a > senkou_b:
		cloud_color = 'green'
	else:
		cloud_color = 'red'

	conversion_bullish = False
	if tenkan_sen > kijun_sen:
		conversion_bullish = True

	bear_bull = 'none'
	if current_price > senkou_a:
		bear_bull = 'bull'
	if current_price < senkou_b:
		bear_bull = 'bear'

	results = {'cloud_color':cloud_color,'bullish_conversion':conversion_bullish,'cloud_analysis':bear_bull}
	return(results)


def get_prices(ticker,days_back):
	today = datetime.datetime.today()
	day_back = today - BDay(days_back)
	#print(day_back)
	date = day_back.strftime("%y-%m-%d")
	filename =  'data/' + date + ticker + '.pickle'
	try:
		with open(filename,'rb') as rfp:
			prices = pickle.load(rfp)
		just_price = []
		for i in prices:
			just_price.append(float(i['last']))
	except:
		just_price = []
	return(just_price)

def back_test(ticker, max_depth_analysis_in_days, tenkan_period):
	owned = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
			'correct_percentage':float(0),'tenkan':tenkan_period,
			'gain_per_trade':0, 'sharpe':0}
	returns = []

	for day in range(0,max_depth_analysis_in_days):
		prices = get_prices(ticker,day)
		for i in range(tenkan_period*6,len(prices)-1):
			blind_prices = prices[:i]
			results = find_sentiment(blind_prices,tenkan_period)
			if owned == {}:
				if results['cloud_color'] == 'green' and results['bullish_conversion'] and results['cloud_analysis'] == 'bull':
					owned = {'i':i,'purchase_price':prices[i]}
					moves += 1
					#print('bought at')
			else:
				if results['cloud_color'] == 'red' or results['bullish_conversion'] == False or results['cloud_analysis'] == 'bear':
					profit_percentage = (prices[i] - owned['purchase_price']) / owned['purchase_price']
					#print('sold at ' + str(prices[i]))
					owned = {}
					total_percent_gain += profit_percentage
					if profit_percentage > 0:
						correct_moves += 1
					returns.append(profit_percentage)
	if moves > min_n:
		response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
		'correct_percentage':float(correct_moves/moves),'tenkan':tenkan_period,
		'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}
	
	return response

def back_test_reverse(ticker, max_depth_analysis_in_days, tenkan_period):
	owned = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
			'correct_percentage':float(0),'tenkan':tenkan_period,
			'gain_per_trade':0, 'sharpe':0}
	returns = []
	for day in range(0,max_depth_analysis_in_days):
		prices = get_prices(ticker,day)
		for i in range(tenkan_period*6,len(prices)-1):
			blind_prices = prices[:i]
			results = find_sentiment(blind_prices,tenkan_period)
			if owned == {}:
				if results['cloud_color'] == 'red' and results['bullish_conversion'] and results['cloud_analysis'] == 'bear':
					owned = {'i':i,'purchase_price':prices[i]}
					moves += 1
					#print('bought at')
			else:
				if results['cloud_color'] == 'green' or results['cloud_analysis'] == 'bull':
					profit_percentage = (prices[i] - owned['purchase_price']) / owned['purchase_price']
					#print('sold at ' + str(prices[i]))
					owned = {}
					total_percent_gain += profit_percentage
					if profit_percentage > 0:
						correct_moves += 1
					returns.append(profit_percentage)
	if moves > min_n:
		response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
		'correct_percentage':float(correct_moves/moves),'tenkan':tenkan_period,
		'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}
	
	return response

def machine_learn(ticker,max_depth_analysis_in_days):
	current_tenkan = 4
	best_result = {}
	reverser = False
	for i in range(0,200):
		#print(str(i) + '/' + str(200))
		current_tenkan += 1

		result = back_test(ticker,max_depth_analysis_in_days,current_tenkan)
		reverse = back_test_reverse(ticker,max_depth_analysis_in_days,current_tenkan)
		if best_result == {} or result['sharpe'] > best_result['sharpe'] :
			best_result = result
			reverser = False
		if reverse['sharpe'] > best_result['sharpe']:
			best_result = reverse
			reverser = True
	return({'best_result':best_result,'reverse':reverser})

def create_game_plan():
	tickers = []
	symbols = open("watchlist.txt").readlines()
	for symbol in symbols:
		symbol = symbol.rstrip("\n")
		tickers.append(symbol)
	#tickers = {'BB':False,'SPY':False,'GME':False}
	decisions = {}
	for ticker in tickers:
		print(ticker)
		results = machine_learn(ticker,4)
		if results['best_result']['correct_moves'] > 5:
			print('pattern detected')
			decisions[ticker] = {'reverse':results['reverse'], 'tenkan_period': results['best_result']['tenkan'],
								   'sharpe':results['best_result']['sharpe'], 'n':results['best_result']['moves']}
		else:
			print(' unable to detect pattern with current dataset')
	with open('game_plan.pickle','wb') as wfp:
		pickle.dump(decisions, wfp)
	return('done')

def create_game_plan_blue():
	tickers = []
	symbols = open("blue_chip_watchlist.txt").readlines()
	for symbol in symbols:
		symbol = symbol.rstrip("\n")
		tickers.append(symbol)
	#tickers = {'BB':False,'SPY':False,'GME':False}
	decisions = {}
	for ticker in tickers:
		print(ticker)
		results = machine_learn(ticker,4)
		if results['best_result']['correct_moves'] > 5:
			print('pattern detected')
			decisions[ticker] = {'reverse':results['reverse'], 'tenkan_period': results['best_result']['tenkan'],
								   'sharpe':results['best_result']['sharpe'], 'n':results['best_result']['moves']}
		else:
			print(' unable to detect pattern with current dataset')
	with open('blue_chip_game_plan.pickle','wb') as wfp:
		pickle.dump(decisions, wfp)
	return('done')