from models.Line import Line


class Candle(Line):
	def __init__(self, data):
		super().__init__(data);
		self.maximalPrice = data[2] 
		self.minimalPrice = data[3]