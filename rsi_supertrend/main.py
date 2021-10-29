import pandas as pd
# import tqdm
# import statistics
# import get_ml_supertrend
# import time
# import csv
import backtest


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

backtest_results = backtest.back_test(df,taxes,back_test_interval,sell_interval)
print(backtest_results)