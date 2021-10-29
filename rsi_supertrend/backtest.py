import buy_function
import sell_function
import tqdm
import statistics

def back_test(data,tax,back_test_interval,sell_interval):
	current_position = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	max_len = 24 * 10 * 100
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
				'correct_percentage':float(0),
				'gain_per_trade':0, 'sharpe':0}
	returns = []

	price_list = data['open'].tolist()
	for i in tqdm.tqdm(range(max_len,len(data),back_test_interval)):
		current_test_set = data[i-(max_len):i]
		try:
			if current_position == {}:
				if buy_function.should_I_buy(current_test_set,sell_interval) and sell_function.should_I_sell(current_test_set,sell_interval, timeperiod=14,fastk_period=14,fastd_period=3,RSI_sell_level=85) == False:
					current_position = {'i':i,'purchase_price':price_list[i]}
					#print('bought')
					moves += 1
			elif current_position != {}:
				#print(current_test_set['close'].iloc[-1])
				if sell_function.should_I_sell(current_test_set,sell_interval, timeperiod=14,fastk_period=14,fastd_period=3,RSI_sell_level=85):
					profit_percentage = (price_list[i] - current_position['purchase_price'] - (price_list[i] * tax)) / current_position['purchase_price']
					total_percent_gain += profit_percentage
					current_position = {}
					#print('sold')
					if profit_percentage > 0:
						correct_moves += 1
					returns.append(profit_percentage)
					#print(profit_percentage)
		except KeyError:
			pass

	try:
		response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
					'correct_percentage':float(correct_moves/moves),
					'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}
	except:
		response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
					'correct_percentage':0,
					'gain_per_trade':0, 'sharpe':0}
	return(response)