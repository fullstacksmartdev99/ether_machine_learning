import supertrend
import statistics
import tqdm

def back_test(data,len1,len2):
	current_position = {}
	total_percent_gain = 0.0
	moves = 0
	correct_moves = 0
	response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
			'correct_percentage':float(0),
			'gain_per_trade':0, 'sharpe':0}
	returns = []

	for i in range(0,len(data)):
		trend = supertrend.up_down_super(data,len1,len2)
		if current_position == {} and trend == 'up':
			current_position = {'i':i,'purchase_price':data[i]}
			print('bought')
			print(current_position)
			moves += 1
		elif current_position != {} and trend == 'down':
			profit_percentage = (data[i] - current_position['purchase_price'] - (data[i] * current_strategy['taxes'])) / current_position['purchase_price']
			total_percent_gain += profit_percentage
			current_position = {}
			if profit_percentage > 0:
				correct_moves += 1
			returns.append(profit_percentage)

	response = {'total_percent_gain':total_percent_gain,'correct_moves':correct_moves,'moves':moves,
				'correct_percentage':float(correct_moves/moves),'tenkan':settings['tenkan'],
				'gain_per_trade':total_percent_gain / moves, 'sharpe':statistics.mean(returns) / statistics.stdev(returns)}
	except:
		response = {'total_percent_gain':0,'correct_moves':0,'moves':0,
				'correct_percentage':0,'tenkan':settings['tenkan'],
				'gain_per_trade':0, 'sharpe':0}
	return(response)