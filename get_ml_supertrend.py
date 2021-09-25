import supertrend
import statistics
import tqdm

def back_test(data,setting,back_test_interval):
	len1 = setting['len1']
	len2 = setting['len2']
	max_len = 0
	if len1 > len2:
		max_len = len1
	else:
		max_len = len2
	max_len = max_len * 3
	current_position = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
			'correct_percentage':float(0),
			'gain_per_trade':0, 'sharpe':0}
	returns = []

	price_list = data['open'].tolist()
	for i in range(max_len,len(data),back_test_interval):
		current_test_set = data[i-(max_len):i]
		try:
			trend = supertrend.up_down_super(current_test_set,len1,len2)

			if current_position == {}:
				if trend == 'up':
					current_position = {'i':i,'purchase_price':price_list[i]}
					#print('bought')
					#print(price_list[i])
					moves += 1
			elif current_position != {}:
				if trend == 'down':
					profit_percentage = (price_list[i] - current_position['purchase_price'] - (price_list[i] * setting['taxes'])) / current_position['purchase_price']
					total_percent_gain += profit_percentage
					current_position = {}
					#print('sold')
					#print(price_list[i])
					if profit_percentage > 0:
						correct_moves += 1
					returns.append(profit_percentage)
		except KeyError:
			pass

	try:
		response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
					'correct_percentage':float(correct_moves/moves),'len1':len1, 'len2':len2,
					'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}
	except:
		response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
				'correct_percentage':0, 'len1':len1, 'len2':len2,
				'gain_per_trade':0, 'sharpe':0}
	return(response)

def all_possible_settings(max_depth,taxes,max_settings_len1,min_multiplier,max_multiplier):
	settings_to_try = []

	interval = int(max_depth / max_settings_len1)

	for len1 in range(interval,max_depth,interval):
		for len2 in range(min_multiplier,max_multiplier):
			settings_to_try.append({'len1':len1,'len2':len2,'taxes':taxes})

	return(settings_to_try)


def learn(data,taxes,max_depth,max_settings_len1,min_multiplier,max_multiplier,back_test_interval,show_progress=True):
	best_settings = {'len1':0,'len2':0}
	best_sharpe = -9999
	best_results = {}

	settings_to_try = []

	minimum_n = 10

	settings_to_try = all_possible_settings(max_depth,taxes,max_settings_len1,min_multiplier,max_multiplier)

	for setting in tqdm.tqdm(settings_to_try):
		result = back_test(data,setting,back_test_interval)
		if result['moves'] > minimum_n:
			if result['sharpe'] > best_sharpe:
				best_sharpe = result['sharpe']
				best_settings = setting
				best_results = result

	return(best_settings,best_results)

