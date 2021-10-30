import pandas as pd

import indicators

# df = pd.read_parquet('ETH-USDT.parquet').tail(100000)

def should_I_buy(df,buy_settings,sell_settings):
	interval = buy_settings['interval']
	RSI_buy_level = buy_settings['RSI_buy_level']
	timeperiod= buy_settings['timeperiod']
	fastk_period= buy_settings['fastk_period']
	fastd_period= buy_settings['fastd_period']
	should_I_buy = False
	trend = indicators.check_side_interval(interval,df)
	if trend == 'up':
		price_list = df['close'].tolist()
		price_list = price_list[0::int(sell_settings['interval'])]
		response = indicators.get_stoch_rsi(price_list,timeperiod,fastk_period,fastd_period)
		if response['SRSI'] < RSI_buy_level and response['past_SRSI'] < RSI_buy_level and response['third_SRSI'] < RSI_buy_level:
			should_I_buy = True
	return(should_I_buy)

# print(should_I_buy(df))