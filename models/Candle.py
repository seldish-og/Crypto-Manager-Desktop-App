from models.Line import Line


class Candle(Line):
	width = 8 

	def __init__(self, data):
		super().__init__(data);
		self.maximalPrice = data[2] 
		self.minimalPrice = data[3]