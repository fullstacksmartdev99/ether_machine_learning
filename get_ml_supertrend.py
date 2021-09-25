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
		if current_position == {}:
