import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.URL = 'https://ru.tradingview.com/ideas/'
        self.HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/87.0.4280.141 Safari/537.36',
                        'accept': '*/*'}
        self.HOST = 'https://ru.tradingview.com'

    def get_html_text(self, url):
        page = requests.get(url, headers=self.HEADERS)
        html_text = page.text
        return html_text

    def save_image(self, link):
        pass

    def find_all_cards(self):
        soup = BeautifulSoup(self.get_html_text(url=self.URL), 'html.parser')
        items = soup.find_all('div', class_='tv-feed-layout__card-item')
        for item in items[4]:
            title = ''
            name = ''
            link = ''
            image = ''
        print(items)

parser = Parser()
parser.find_all_cards()