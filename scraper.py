from RBKNewsScraper import RBKNewsScraper, NewsItem

#Создаем объект скэппера, он автоматически парсит 15 новостей с главной страницы
news = RBKNewsScraper()

#Теперь мы можем с ним работать

#Вывод новостей на стандартный вывод
news.print_all_news()

#Возвращение списка новостей в виде списка со словарями
d = news.get_list()


#Возвращение списка новостей в виде JSON
j = news.get_json()