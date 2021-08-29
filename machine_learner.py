import pandas as pd
import ichi_indicator
import statistics
import tqdm

def back_test(data,settings,step):
	owned = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
			'correct_percentage':float(0),'tenkan':settings['tenkan'],
			'gain_per_trade':0, 'sharpe':0}
	returns = []

	for i in range(settings['tenkan'] * 6,len(data) - 1):
		price = data[i]
		blind_prices = data[:i]
		sentiment = ichi_indicator.find_sentiment(blind_prices,settings['tenkan'])
		if owned == {}:
			if sentiment == settings['sentiment']:
				owned = {'i':i,'purchase_price':data[i]}
				moves += 1
		else:
			if sentiment != settings['sentiment']:
				profit_percentage = (data[i] - owned['purchase_price'] - (data[i] * settings['taxes'])) / owned['purchase_price']
				total_percent_gain += profit_percentage
				owned = {}
				if profit_percentage > 0:
					correct_moves += 1
				returns.append(profit_percentage)

	try:
		response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
					'correct_percentage':float(correct_moves/moves),'tenkan':settings['tenkan'],
					'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}
	except:
		response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
					'correct_percentage':0,'tenkan':settings['tenkan'],
					'gain_per_trade':0, 'sharpe':0}

	return(response)


def all_possible_settings(tenkans, taxes,step):

	settings_to_try = []


	cloud_color = 'green'
	bullish_conversion = True
	cloud_analysis = 'bull'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	cloud_color = 'green'
	bullish_conversion = True
	cloud_analysis = 'bear'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	cloud_color = 'green'
	bullish_conversion = False
	cloud_analysis = 'bull'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	cloud_color = 'green'
	bullish_conversion = False
	cloud_analysis = 'bear'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	cloud_color = 'red'
	bullish_conversion = True
	cloud_analysis = 'bull'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	cloud_color = 'red'
	bullish_conversion = False
	cloud_analysis = 'bull'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	cloud_color = 'red'
	bullish_conversion = True
	cloud_analysis = 'bear'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	cloud_color = 'red'
	bullish_conversion = False
	cloud_analysis = 'bear'
	for tenkan in tenkans:
		setting = {'tenkan':tenkan, 'taxes':taxes, 'sentiment':{'cloud_color':cloud_color,'bullish_conversion':bullish_conversion,'cloud_analysis':cloud_analysis}}
		settings_to_try.append(setting)

	return(settings_to_try)


def learn(data,taxes,show_progress=True,backtest_step=10,step=1):
	best_settings = {'tenkan':0, 'taxes':0.001, 'sentiment':{'cloud_color':'none','bullish_conversion':False,'cloud_analysis':'none'}}
	best_sharpe = -9999
	best_results = {}

	max_tenkan = int(len(data) / 50)

	tenkans = []

	i = 4
	while i < max_tenkan:
		i = int(i * 1.5)
		tenkans.append(i)


	minimum_n = 10

	settings_to_try = all_possible_settings(tenkans,taxes,step)

	if show_progress:
		for setting in tqdm.tqdm(settings_to_try):
			result = back_test(data,setting,step)
			if result['moves'] > minimum_n:
				if result['sharpe'] > best_sharpe:
					best_sharpe = result['sharpe']
					best_settings = setting
					best_results = result
	else:
		for setting in settings_to_try:
			result = back_test(data,setting,step)
			if result['moves'] > minimum_n:
				if result['sharpe'] > best_sharpe:
					best_sharpe = result['sharpe']
					best_settings = setting
					best_results = result

	# print(f'your best sharpe is {best_sharpe}')
	# print(best_settings)
	# print(best_results)

	return(best_settings)


