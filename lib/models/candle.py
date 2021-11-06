from . import Line


class Candle(Line):
	width = 8 

	def __init__(self, data):
		super().__init__(data);
		self.maximalPrice = float(data[2])
		self.minimalPrice = float(data[3])