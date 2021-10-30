import buy_function
import sell_function
import tqdm
import statistics

def back_test(data,tax,back_test_interval,buy_settings,sell_settings):
	current_position = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	max_len = 24 * 10 * 100
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
				'correct_percentage':float(0),
				'gain_per_trade':0, 'sharpe':0}
	returns = []

	account_value = 1000000
	account_value_list = []
	account_movement_list = []
	movement_dollars = []
	last_account_value = 1000000

	price_list = data['open'].tolist()
	for i in tqdm.tqdm(range(max_len,len(data),back_test_interval)):
		current_test_set = data[i-(max_len):i]
		try:
			if current_position == {}:
				if buy_function.should_I_buy(current_test_set,buy_settings) and sell_function.should_I_sell(current_test_set, sell_settings) == False:
					current_position = {'i':i,'purchase_price':price_list[i]}
					#print('bought')
					moves += 1
			elif current_position != {}:
				#print(current_test_set['close'].iloc[-1])
				if sell_function.should_I_sell(current_test_set,sell_settings):
					profit_percentage = (price_list[i] - current_position['purchase_price'] - (price_list[i] * tax)) / current_position['purchase_price']
					total_percent_gain += profit_percentage
					last_account_value = account_value
					account_value = account_value * (1 + total_percent_gain)
					current_position = {}
					#print('sold')
					if profit_percentage > 0:
						correct_moves += 1
					returns.append(profit_percentage)
					#print(profit_percentage)
		account_value_list.append(account_value)
		account_movement_list.append(1-((account_value-last_account_value)/last_account_value))
		movement_dollars.append((account_value-last_account_value))

		except KeyError:
			pass

	try:
		wins = 0
		losses = 0
		for i in movement_dollars:
			if i > 0:
				wins += i
			elif i < 0:
				losses += abs(i)
		profit_ratio = wins / losses

		response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
					'correct_percentage':float(correct_moves/moves),
					'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(account_movement_list) / statistics.stdev(account_movement_list),
					'profit_ratio': profit_ratio, 'account_value_list':account_value_list 
					}
	except:
		response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
					'correct_percentage':0,
					'gain_per_trade':0, 'sharpe':0}
	return(response)