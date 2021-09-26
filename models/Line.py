class Line:
	width = 9

	def __init__(self, data):
		self.openPrice = data[1]
		self.closePrice = data[4]
		