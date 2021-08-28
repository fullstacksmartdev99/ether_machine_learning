import machine_learner
import pandas as pd
import tqdm
import ichi_indicator

df = pd.read_parquet('ETH-USDT.parquet')

price_list = df['close'].tolist()

taxes = 0.000
data = price_list[:-1]
data = price_list[-129600:-1]

# learned = machine_learner.learn(data,taxes,show_progress=True,backtest_step=1,step=1)

analysis_depth = 10000
# print(learned)

recalculate_every = 60
need_to_recalculate = True
recalculate_timer = 0


current_strategy = {}
current_position = {}
owned = {}
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
			owned = {'i':i,'purchase_price':data[i]}
			moves += 1
	else:
		if sentiment != current_strategy['sentiment']:
			profit_percentage = (data[i] - owned['purchase_price'] - (data[i] * current_strategy['taxes'])) / owned['purchase_price']
			total_percent_gain += profit_percentage
			owned = {}
			if profit_percentage > 0:
				correct_moves += 1
			returns.append(profit_percentage)
	
response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
			'correct_percentage':float(correct_moves/moves),
			'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}

print(returns)
print(response)



