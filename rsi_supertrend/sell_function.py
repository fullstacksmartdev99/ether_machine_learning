import pandas as pd

import indicators

# df = pd.read_parquet('ETH-USDT.parquet').tail(100000)

def should_I_sell(df,sell_settings):
	interval = sell_settings['interval']
	timeperiod=sell_settings['timeperiod']
	fastk_period=sell_settings['fastk_period']
	fastd_period=sell_settings['fastd_period']
	RSI_sell_level=sell_settings['RSI_sell_level']
	df = df[0::int(interval)]
	should_I_sell = False
	price_list = df['close'].tolist()
	response = indicators.get_stoch_rsi(price_list,timeperiod,fastk_period,fastd_period)
	if response['SRSI'] > RSI_sell_level or response['past_SRSI'] > RSI_sell_level or response['third_SRSI'] > RSI_sell_level:
		if response['bearish_crossover'] or response['past_bearish_crossover']:
			should_I_sell = True
	return(should_I_sell)

# print(should_I_sell(df,5))