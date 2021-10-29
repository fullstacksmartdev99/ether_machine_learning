import talib
import supertrend
import numpy

def get_stoch_rsi(close,timeperiod,fastk_period,fastd_period):
	close = numpy.array([float(x) for x in close])
	if len(close) < 4*timeperiod:
		print('len too far')
		return('NaN')
	else:
		fastk, fastd = talib.STOCHRSI(close, timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=0)
		SMA = talib.SMA(fastd,timeperiod=3)
		bullish_crossover = False
		bearish_crossover = False
		past_bearish_crossover = False
		past_bullish_crossover = False
		#bullish scenario
		if fastd[-1] > SMA[-1]:
			if fastd[-2] < SMA[-2]:
				bullish_crossover = True
		#bearish scenario
		if fastd[-1] < SMA[-1]:
			if fastd[-2] > SMA[-2]:
				bearish_crossover = True

		#get last section bullish/bearish scenarios
		#bullish scenario
		if fastd[-2] > SMA[-2]:
			if fastd[-3] < SMA[-3]:
				past_bullish_crossover = True
		#bearish scenario
		if fastd[-2] < SMA[-2]:
			if fastd[-3] > SMA[-3]:
				past_bearish_crossover = True

		return({'SRSI':fastd[-1],'SMA':SMA[-1],'bullish_crossover':bullish_crossover,
			    'bearish_crossover':bearish_crossover, 'past_bearish_crossover':past_bearish_crossover,
			    'past_bullish_crossover':past_bullish_crossover, 'past_SRSI':fastd[-2], 'third_SRSI':fastd[-3]})

def check_side_interval(interval,current_data):
	current_data = current_data[0::interval]
	periods = 14
	multiplier = 4
	if interval < 10 and interval > 1:
		period = 12
		multiplier = 3
	elif interval < 30 and interval > 9:
		period = 10
		multiplier = 4
	elif interval < 60 and interval > 29:
		period = 10
		multiplier = 3
	elif interval < 120 and interval > 59:
		period = 8
		multiplier = 4
	elif interval < 360 and interval > 119:
		period = 12
		multiplier = 4
	elif interval < 420 and interval > 359:
		period = 10
		multiplier = 4
	elif interval < 700 and interval > 419:
		period = 6
		multiplier = 3
	elif interval > 699:
		period = 12
		multiplier = 4
	trend = supertrend.up_down_super(current_data,period,multiplier)
	return(trend)