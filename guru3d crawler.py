import requests
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page = 1

    while page <= max_pages:
        url = 'https://www.guru3d.com/news-page/' + str(page) + '.html'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")

        for div in soup.findAll('div', {'class': 'content'}):

            for link in div.findAll('a'):
                href = "https://www.guru3d.com/" + str(link.get('href'))
                print(href)
        page += 1

trade_spider(1)
