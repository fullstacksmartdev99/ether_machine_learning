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