from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime, json

class NewsItem:


    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.date = None
        self.paragraphs = []
        self.text_short = None

    #Возвращает новость в виде словаря
    def get_dict(self):
        out = {'title': self.title, 'link': self.link, 'date': self.date, 'short': self.text_short}
        text = ""
        for paragraph in self.paragraphs:
            text += paragraph
        out['text'] = text

        return out

    #Вывод на пеать при print()
    def __str__(self):
        output = "Заголовок: " + "\n"
        output += self.title + "\n\n"
        output += self.link + "\n\n"
        output += "Дата публикации: " + self.date.strftime("%d-%m-%Y %H:%M") + "\n\n"
        output += "Коротко: " + "\n"
        output += self.text_short + "\n\n"
        output += "Полный текст: " + "\n"
        for paragraph in self.paragraphs:
            output += paragraph + "\n"
        output += "------" + "\n\n"
        return  output






class RBKNewsScraper:


    def __init__(self, url="https://www.rbc.ru/"):
        self.news = []
        self.index_page_url = url
        main_page_urlopened = urlopen(self.index_page_url)
        self.soup = BeautifulSoup(main_page_urlopened, 'html.parser')

        #Добавляем заголовок и ссылку основной новости (выделенна жирным на главной странце)
        first_news_item_soup = self.soup.find(class_="main__big__link")
        first_news_item = NewsItem(str.strip(first_news_item_soup.text), first_news_item_soup.attrs['href'])
        self.news.append(first_news_item)

        #Доавляем заголовки и ссылки на остальные новости
        other_news_soup = self.soup.find_all(class_="main__feed")
        for news_item_soup in other_news_soup:
            news_item_title = str.strip(news_item_soup.text)
            news_item_link  = news_item_soup.find(class_='main__feed__link').attrs['href']
            news_item = NewsItem(news_item_title, news_item_link)
            self.news.append(news_item)

        #Для всех добавленных новостей добавляем дату написания и текст новости
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
            #Добавляев в объекты новостей дату
            news_item.date = RBKNewsScraper.create_date(raw_date)

            #Добаввляем краткий вариант новости
            news_item.text_short =   str.strip(news_item_soup.find(class_="article__text__overview").text)

            #Добавлем основной текст новости
            paragraphs_soup_all =  news_item_soup.find_all(class_="article__text")
            for paragraph_soup in paragraphs_soup_all:
                paragraphs = paragraph_soup.find_all('p')
                for paragraph in paragraphs:
                    #Не вставляем параграф если это баннер (опытнм путем установлено что в этом случае в параграфе присутсвует "\n\n\n\n")
                    if paragraph.text.find("\n\n\n\n") == -1:
                        news_item.paragraphs.append(paragraph.text)

    #Для вывода всего на печать в консоль
    def print_all_news(self):
        for item in self.news:
            print(item)


    #Возвращает лист с новостями в  виде словарей
    def get_list(self):
        out = []
        for item in self.news:
            out.append(item.get_dict())
        return out

    #Возвращает новсти в JSON формате
    def get_json(self):
        news = self.get_list()
        for item in news:
            item['date'] = str(item['date'])
        json_news = json.dumps(news)
        return json_news



