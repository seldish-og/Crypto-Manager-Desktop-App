import sys

import requests

from .Connection import Connection
from .Repository import Repository


class ChartRepository(Repository):
    def __init__(self) -> None:
        pass

    def getRemoteData(self) -> str:
        response = requests.get(Connection.FETCH_CHART_URL)
        return response.content
