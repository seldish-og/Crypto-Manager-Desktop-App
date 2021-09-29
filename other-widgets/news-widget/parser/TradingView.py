import requests
from bs4 import BeautifulSoup
import lxml
import cchardet


class Parser:
    def __init__(self):
        self.URL = 'https://ru.tradingview.com/ideas/'
        self.HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/87.0.4280.141 Safari/537.36',
                        'accept': '*/*'}
        self.HOST = 'https://ru.tradingview.com'

    def get_html_text(self, url):
        requests_session = requests.Session()
        page = requests_session.get(url, headers=self.HEADERS)
        html_text = page.text
        return html_text

    def save_image(self, link):
        pass

    def find_all_cards(self):
        soup = BeautifulSoup(self.get_html_text(url=self.URL), 'lxml')
        items = soup.find_all('div', class_='tv-feed-layout__card-item')
        for item in items[:1]:
            article_title = soup.find('a', class_='tv-widget-idea__title').get_text(strip=True)
            crypto_name = soup.find('a', class_='tv-widget-idea__symbol').get_text(strip=True)
            article_link = self.HOST + item.find('a', class_='tv-widget-idea__title').get('href')
            article_image_link = soup.find('img', 'tv-widget-idea__cover').get('data-src')
            print(article_title)
            print(crypto_name)
            print(article_link)
            print(article_image_link)


parser = Parser()
parser.find_all_cards()