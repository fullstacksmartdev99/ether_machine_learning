import machine_learner
import pandas as pd
import tqdm
import ichi_indicator
import statistics

df = pd.read_parquet('ETH-USDT.parquet')

price_list = df['close'].tolist()

taxes = 0.000
data = price_list[:-1]
data = price_list[-(60 * 24 * 365):-1]

# learned = machine_learner.learn(data,taxes,show_progress=True,backtest_step=1,step=1)

analysis_depth = 3000
# print(learned)

recalculate_every = 360


def get_calculation(recalculate_every, analysis_depth):
	need_to_recalculate = True
	recalculate_timer = 0


	current_strategy = {}
	current_position = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
				'correct_percentage':float(0),
				'gain_per_trade':0, 'sharpe':0}
	returns = []

	for i in tqdm.tqdm(range(analysis_depth,len(data))):
		if recalculate_timer > recalculate_every:
			need_to_recalculate = True
		if need_to_recalculate:
			current_strategy = machine_learner.learn(data[i-analysis_depth:i],taxes,show_progress=True,backtest_step=1,step=1)
			need_to_recalculate = False
			recalculate_timer = 0
		recalculate_timer += 1

		if current_position == {}:
			sentiment = ichi_indicator.find_sentiment(data[i-analysis_depth:i],current_strategy['tenkan'])
			if sentiment == current_strategy['sentiment']:
				current_position = {'i':i,'purchase_price':data[i]}
				print('bought')
				print(current_position)
				moves += 1
		else:
			if sentiment != current_strategy['sentiment']:
				print('sold')
				print(data[i])

				profit_percentage = (data[i] - current_position['purchase_price'] - (data[i] * current_strategy['taxes'])) / current_position['purchase_price']
				total_percent_gain += profit_percentage
				current_position = {}
				if profit_percentage > 0:
					correct_moves += 1
				returns.append(profit_percentage)
		
	response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
				'correct_percentage':float(correct_moves/moves),
				'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}

	return(response)


# recalculate_everys = []
# analysis_depths = []
# for i in range(1,10):
# 	recalculate_everys.append(60*i)
# 	analysis_depths.append(1000 * i)

# best_response = {'sharpe':0}
# best_settings = {'recalculate_every':0,'analysis_depth':0}


# iteration = 0
# for recalculate_every in recalculate_everys:
# 	for analysis_depth in analysis_depths:
# 		print('trying number ' + str(iteration) + ' out of ' + str(len(recalculate_everys) * len(analysis_depths)))
# 		response = get_calculation(recalculate_every,analysis_depth)
# 		if response['sharpe'] > best_response['sharpe']:
# 			best_settings = {'recalculate_every':recalculate_every,'analysis_depth':analysis_depth}
# 			best_response = response

# print(best_settings)
# print(best_response)

results = get_calculation(480,8000)

print(results)



