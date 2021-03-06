import re

class Connection:
	FETCH_CHART_URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h"
	PREVIOUS_CHART_URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h"
	SYMBOLS_URL = "https://api3.binance.com/api/v3/ticker/price"

	def __init__(self) -> None:
		pass

	@staticmethod
	def updateTimeStamp(timeStamp):
		Connection.FETCH_CHART_URL = re.sub(r"interval=[A-Za-z0-9]+", "interval=" + timeStamp, Connection.FETCH_CHART_URL)
		print(Connection.FETCH_CHART_URL, timeStamp)

	@staticmethod
	def updateCurrency(currency):
		Connection.FETCH_CHART_URL = re.sub(r"symbol=[A-Za-z0-9]+\&", "symbol=" + currency, Connection.FETCH_CHART_URL)