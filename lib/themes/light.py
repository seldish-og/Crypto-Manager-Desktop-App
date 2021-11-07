from . import Theme

class Light(Theme):
	def __init__(self, backgroundColor = "#fff", chartLineColor = "#0695b8", gridLineColor = "#45293442", currentPriceLineColor="#2f3947", bearColor = "#ef5350", bullColor ="#26a69a", textColor = "#000") -> None:
		super().__init__(backgroundColor, chartLineColor, gridLineColor, currentPriceLineColor, bearColor, bullColor, textColor)	