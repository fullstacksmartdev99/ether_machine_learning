import pandas as pd
import ichi_indicator
import machine_learner
import json


df = pd.read_parquet('ETH-USDT.parquet')

price_list = df['close'].tolist()

taxes = 0.0
data = price_list[-10000:-1]


learned_setting = machine_learner.learn(data,taxes,step=20)

with open('endpoint.json', 'w') as fp:
    json.dump(learned_setting, fp)