import pandas as pd
import tqdm
import statistics
import get_ml_supertrend
import time
import supertrend

df = pd.read_parquet('ETH-USDT.parquet')
print(df)
#df = df.tail(365*24*60)

taxes = 0.000

max_depth = 14
max_settings_len1 = 5
min_multiplier = 2
max_multiplier = 5
back_test_interval = 1


def check_side_interval(interval,current_data):
	current_data = current_data[0::interval]
	periods = 14
	multiplier = 4
	if interval < 10 and interval > 1:
		period = 12
		multiplier = 3
	elif interval < 30 and interval > 9:
		period = 10
		multiplier = 4
	elif interval < 60 and interval > 29:
		period = 10
		multiplier = 3
	elif interval < 120 and interval > 59:
		period = 8
		multiplier = 4
	elif interval < 360 and interval > 119:
		period = 12
		multiplier = 4
	elif interval < 420 and interval > 359:
		period = 10
		multiplier = 4
	elif interval < 700 and interval > 419:
		period = 6
		multiplier = 3
	elif interval > 699:
		period = 12
		multiplier = 4
	trend = supertrend.up_down_super(current_data,period,multiplier)
	return(trend)

def back_test(data,tax,back_test_interval):
	current_position = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	max_len = 12 * 4 * 100
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
			'correct_percentage':float(0),
			'gain_per_trade':0, 'sharpe':0}
	returns = []

	price_list = data['open'].tolist()
	for i in range(max_len,len(data),back_test_interval):
		current_test_set = data[i-(max_len):i]
		try:
			trend = check_side_interval(back_test_interval,current_test_set)
			if current_position == {}:
				if trend == 'up':
					current_position = {'i':i,'purchase_price':price_list[i]}
					print('bought')
					#print(price_list[i])
					moves += 1
			elif current_position != {}:
				if trend == 'down':
					profit_percentage = (price_list[i] - current_position['purchase_price'] - (price_list[i] * tax)) / current_position['purchase_price']
					total_percent_gain += profit_percentage
					current_position = {}
					print('sold')
					#print(price_list[i])
					if profit_percentage > 0:
						correct_moves += 1
					returns.append(profit_percentage)
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


def should_I_sell(current_data,tax=0.0,intervals_to_check=[420]):
	signal = False
	down = True
	for i in intervals_to_check:
		if down:
			trend = check_side_interval(i,current_data)
			if trend == 'up':
				down = False
	if down:
		signal = True

	# back_test_interval = 10
	# result = back_test(current_data,tax,back_test_interval)
	return(signal)

def should_I_buy(buy_interval, current_data):
	trend = check_side_interval(buy_interval,current_data)
	signal = False
	if trend == 'up':
		signal = True
	return(signal)

def full_backtest(data,tax,back_test_interval,intervals_to_check):
	current_position = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	max_len = 12 * 4 * 100
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
			'correct_percentage':float(0),
			'gain_per_trade':0, 'sharpe':0}
	returns = []

	price_list = data['open'].tolist()
	for i in tqdm.tqdm(range(max_len,len(data),back_test_interval)):
		current_test_set = data[i-(max_len):i]
		try:
			if current_position == {}:
				if should_I_buy(420,current_test_set):
					current_position = {'i':i,'purchase_price':price_list[i]}
					# print('bought')
					#print(price_list[i])
					moves += 1
			elif current_position != {}:
				if should_I_sell(current_test_set,0.0,intervals_to_check):
					profit_percentage = (price_list[i] - current_position['purchase_price'] - (price_list[i] * tax)) / current_position['purchase_price']
					total_percent_gain += profit_percentage
					current_position = {}
					# print('sold')
					#print(price_list[i])
					if profit_percentage > 0:
						correct_moves += 1
					returns.append(profit_percentage)
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


intervals_to_check = [
						[420],
						[360],
						[120],
						[60],
						[30],
						[10],
						[5],
						[360,120,60,30,10,5],
						[120,60,30,10,5],
						[30,10,5],
						[10,5],
						[120,60,30,10],
						[60,30,10],
						[30,10],
						[10],
						[5]
					 ]

df = df.tail(1000000)
test = full_backtest(df,0,5,intervals_to_check)
print(test)

