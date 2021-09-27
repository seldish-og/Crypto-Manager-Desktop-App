import re

class Connection:
	FETCH_CHART_URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m"

	def __init__(self) -> None:
		pass

	@staticmethod
	def updateTimeStamp(timeStamp):
		Connection.FETCH_CHART_URL = re.sub(r"interval=[A-Za-z0-9]+", "interval=" + timeStamp, Connection.FETCH_CHART_URL)
		print(Connection.FETCH_CHART_URL, timeStamp)