from urllib.request import urlopen
from bs4 import BeautifulSoup

class NewsItem:


    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.date = None
        self.text = None

    def add_date(self, date):
        self.date = date

    def add_text(self, text):
        self.text = text

    def get_all(self):
        return {'title': self.title, 'link': self.link, 'date': self.date, 'text': self.text}




class RBKNewsScraper:


    def __init__(self, url="https://www.rbc.ru/"):
        self.news = {}
        self.index_page_url = url
        self.main_page = urlopen(self.index_page_url)
        self.soup = BeautifulSoup(self.main_page, 'html.parser')

        #Добавляем в список новостей основную новость (выделенна жирным на главной странце)
        self.first_news_item_soup = self.soup.find(class_="main__big__link")
        self.first_news_item = NewsItem(str.strip(self.first_news_item_soup.text), self.first_news_item_soup.attrs['href'])
        self.news['1'] = self.first_news_item





    def scrap_news_list(self):
        pass

    def scrap_news_item(self, url):
        pass