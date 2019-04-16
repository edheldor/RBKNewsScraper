from urllib.request import urlopen
from bs4 import BeautifulSoup
import re, datetime

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
        self.news = []
        self.index_page_url = url
        main_page_urlopened = urlopen(self.index_page_url)
        self.soup = BeautifulSoup(main_page_urlopened, 'html.parser')

        #Добавляем основную новость (выделенна жирным на главной странце)
        first_news_item_soup = self.soup.find(class_="main__big__link")
        first_news_item = NewsItem(str.strip(first_news_item_soup.text), first_news_item_soup.attrs['href'])
        self.news.append(first_news_item)

        #Доавляем остальные новости
        other_news_soup = self.soup.find_all(class_="main__feed")
        for news_item_soup in other_news_soup:
            news_item_title = str.strip(news_item_soup.text)
            news_item_link  = news_item_soup.find(class_='main__feed__link').attrs['href']
            news_item = NewsItem(news_item_title, news_item_link)
            self.news.append(news_item)

        #Для всех добавленных новостей добавляем дату написания и основной текст новости
        self.__scrap_text_and_date_for_all_news()

    @staticmethod
    def create_date (raw_date):
        #Из URL парсится дата, объединятеся с временем и возвращается объект datetime
        raw_date, raw_time = raw_date.split("T")
        time = raw_time[:8]
        timezone = raw_time[8:]
        date = raw_date.replace("-", "/") + "/"
        time = time.replace(":","/") + "/"
        date_and_time_string =  date + time + timezone
        date = datetime.datetime.strptime(date_and_time_string,"%Y/%m/%d/%H/%M/%S/%z")
        return date



    def __scrap_text_and_date_for_all_news(self):
        for news_item in self.news:
            news_item_urlopened = urlopen(news_item.link)
            news_item_soup = BeautifulSoup(news_item_urlopened, 'html.parser')
            raw_date = news_item_soup.find(class_="article__header__date")['content']
            news_item.date = RBKNewsScraper.create_date(raw_date)



