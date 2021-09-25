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

get_trend