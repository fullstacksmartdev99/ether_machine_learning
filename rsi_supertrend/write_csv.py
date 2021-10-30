import csv


def write_history(name,dates,history):
	with open(name, 'w',) as f:
		wr = csv.writer(f)
		for i in range(0,len(history)):
			wr.writerow([dates[i],history[i]])

def print_basic_results(backtest_results):
	print('total profit %')
	print(backtest_results['total_percent_gain'])
	print('correct moves')
	print(backtest_results['correct_moves'])
	print('total moves')
	print(backtest_results['moves'])
	print('gain per trade')
	print(backtest_results['gain_per_trade'])
	print('sharpe')
	print(backtest_results['sharpe'])
	print('profit ratio')
	print(backtest_results['profit_ratio'])