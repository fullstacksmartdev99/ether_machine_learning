import pandas as pd

import indicators

# df = pd.read_parquet('ETH-USDT.parquet').tail(100000)

def should_I_buy(df,interval,RSI_buy_level=40,timeperiod=14,fastk_period=14,fastd_period=3):
	should_I_buy = False
	trend = indicators.check_side_interval(420,df)
	if trend == 'up':
		price_list = df['close'].tolist()
		response = indicators.get_stoch_rsi(price_list,timeperiod,fastk_period,fastd_period)
		if response['SRSI'] < RSI_buy_level and response['past_SRSI'] < RSI_buy_level and response['third_SRSI'] < RSI_buy_level:
			should_I_buy = True
	return(should_I_buy)

# print(should_I_buy(df))