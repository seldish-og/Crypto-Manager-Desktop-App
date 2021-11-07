from . import Theme

class Dark(Theme):
	def __init__(self, backgroundColor = "#111e2e", chartLineColor = "#0695b8", gridLineColor = "#80293442", currentPriceLineColor="#2f3947", bearColor = "#ef5350", bullColor ="#26a69a", textColor = "#fff") -> None:
		super().__init__(backgroundColor, chartLineColor, gridLineColor, currentPriceLineColor, bearColor, bullColor, textColor)	