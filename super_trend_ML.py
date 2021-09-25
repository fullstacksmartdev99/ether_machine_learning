import pandas as pd
import tqdm
import statistics
import get_ml_supertrend
import time

df = pd.read_parquet('ETH-USDT.parquet')
print(df)
df = df.tail(100000)

taxes = 0.000

max_depth = 14
max_settings_len1 = 5
min_multiplier = 2
max_multiplier = 5
back_test_interval = 1

data_interval = 60



def find_best_interval():
	starting_interval = 20
	ending_interval = 720
	intervals = [starting_interval]
	while intervals[-1] < ending_interval:
		intervals.append(intervals[-1] + starting_interval)


	best_interval = 10
	best_results = {}

	for data_interval in tqdm.tqdm(intervals):
		data_frame = df.iloc[::data_interval, :]
		best_settings, best_result = get_ml_supertrend.learn(data_frame,taxes,max_depth,max_settings_len1,min_multiplier,max_multiplier,back_test_interval,show_progress=True)
		if best_result['sharpe'] > best_results['sharpe']:
			best_results = best_result
			best_interval = data_interval

	print(f'best interval was {best_interval}')
	print(best_results)
	return(best_interval)


find_best_interval()

# start = time.time()
# best_settings, best_result = get_ml_supertrend.learn(df,taxes,max_depth,max_settings_len1,min_multiplier,max_multiplier,back_test_interval,show_progress=True)
# print(best_result)
# print(best_settings)
# end = time.time()
# delta = end - start
# print(f"took {delta} seconds to process")