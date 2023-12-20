from bot.Indicators import AddIndicator

class BBRSIStrategy:
	""" Bollinger Bands x RSI Indicator 
		Params
		--
			`rsi_len` = length of RSI
			`bb_len` = length of RBollinger Bands
			`rsi_ob` = Overbought level of RSI	
			`rsi_os` = Oversold level of RSI	
	"""
	def __init__(self, 	
		rsiLen = 8, 
		bbLen = 100, 
		rsiOb = 50, 
		rsiOs = 50):
		self.rsi_ob = rsiOb
		self.rsi_os = rsiOs
		self.bb_len = bbLen
		self.rsi_len = rsiLen


	def setup(self, df):
		self.df = df
		AddIndicator(self.df, "rsi", "rsi", 'close', self.rsi_len)
		AddIndicator(self.df, "lbb", "lbb", 'close', self.bb_len)
		AddIndicator(self.df, "ubb", "ubb", 'close', self.bb_len)


	def getIndicators(self):
		return [
			dict(name="rsi", title="RSI", yaxis="y3"),
			dict(name="lbb", title="Low Boll", color='gray'),
			dict(name="ubb", title="Upper Boll", color='gray'),
		]

	def checkBuySignal(self, i):
		df = self.df
		if (df["rsi"][i] > self.rsi_os) and \
			(df["rsi"][i-1] <= self.rsi_os) and \
			(df['open'][i] < df["lbb"][i] < df['close'][i]):
			return df["close"][i]
	
		return False
		
	def checkSellSignal(self, i):
		df = self.df
		if (df["rsi"][i] < self.rsi_ob) and \
			(df["rsi"][i-1] >= self.rsi_ob) and \
			(df["close"][i] < df["ubb"][i] < df["open"][i]):
			return df["close"][i]
	
		return False

	def getBuySignalsList(self):
		df = self.df
		length = len(df) - 1
		signals = []
		for i in range(1, length):
			res = self.checkBuySignal(i)
			if res:
				signals.append([df['time'][i], df['close'][i]])

		return signals

	def getSellSignalsList(self):
		df = self.df
		length = len(df) - 1
		signals = []
		for i in range(1, length):
			res = self.checkSellSignal(i)
			if res:
				signals.append([df['time'][i], df['close'][i]])

		return signals