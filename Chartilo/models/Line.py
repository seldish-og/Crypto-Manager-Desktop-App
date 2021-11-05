class Line:
	width = 9

	def __init__(self, data):
		self.openPrice = float(data[1])
		self.closePrice = float(data[4])
		