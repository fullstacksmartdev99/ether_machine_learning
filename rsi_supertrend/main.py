import pandas as pd
# import tqdm
# import statistics
# import get_ml_supertrend
# import time
# import csv
import backtest
import write_csv

df = pd.read_parquet('ETH-USDT.parquet')
df = df.tail(100000)

#####
#SETTINGS
#####

taxes = 0.000

max_depth = 14
max_settings_len1 = 5
min_multiplier = 2
max_multiplier = 5
back_test_interval = 1
sell_interval = 420

buy_settings = {
					'interval': 420,
					'RSI_buy_level': 50,
					'timeperiod': 14,
					'fastk_period': 3,
					'fastd_period': 3
				}
sell_settings = {	
					'interval': 420,
					'timeperiod': 14,
					'fastk_period': 3,
					'fastd_period': 3,
					'RSI_sell_level': 85
					
				}

intervals = [10,30,50,75,100,150,200,250,300,600]

for i in intervals:
	sell_settings['interval'] = i
	print('######################################################')
	print('sell_interval')
	print(i)
	print('######################################################')
	backtest_results = backtest.back_test(df,taxes,back_test_interval,buy_settings,sell_settings)
	write_csv.print_basic_results(backtest_results)
	write_csv.write_history(f'{i}history.csv',backtest_results['dates'],backtest_results['account_value_list'])