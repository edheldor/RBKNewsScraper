# RBKNewsScraper
Позволяет получить 15 новостей с главной страницы сайта  https://www.rbc.ru/

# Зависимости
Зависимости указаны в файле requirements.txt

Тестировалось на python 3.7 и beautifulsoup4 версии 4.7.1

# Использование
Пример использования в файле **scraper.py**


Импортируем все из RBKNewsScraper

`from RBKNewsScraper import RBKNewsScraper, NewsItem`

Создаем объект скэппера, он автоматически парсит 15 новостей с главной страницы

`news = RBKNewsScraper()`


Теперь можно с ним работать

Вывод новостей на стандартный вывод

`news.print_all_news()`

Возвращение списка новостей в виде списка со словарями

`d = news.get_list()`


Возвращение списка новостей в виде строки JSON

`j = news.get_json()`


