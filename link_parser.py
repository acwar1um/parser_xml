import requests
from lxml import html
from datetime import datetime, timedelta


# Начальная дата и количество ссылок для парсинга, идет по дате вниз
start_date = "02.03.2025"
links_to_collect = 10000 


 # Извлечение ссылок из дата-блока
def get_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        links = tree.xpath('//div[@data-block-el="articleTeaser"]//a/@href')
        return links
    else:
        print(f"Ошибка {response.status_code}: Не удалось получить страницу")
        return []

# Сохранение ссылок в файл
def save_links_to_file(links, filename="links.txt"):
    with open(filename, "a", encoding="utf-8") as file:
        for link in links:
            file.write(link + "\n")
    print(f"Ссылки сохранены в {filename}")

# Преобразуем строку с датой в объект datetime
date_obj = datetime.strptime(start_date, "%d.%m.%Y")

all_links = []  # Сбор ссылок
days_passed = 0  # Счётчик дней

# Цикл для прокрутки дат
while len(all_links) < links_to_collect:
    # Формируем URL для каждой даты
    date_str = (date_obj - timedelta(days=days_passed)).strftime("%d.%m.%Y")
    url = f"https://www.spiegel.de/nachrichtenarchiv/artikel-{date_str}.html"
    
    print(f"Парсинг новостей для даты {date_str} из URL: {url}")
    
    # Получаем ссылки на новости
    links = get_links(url)
    
    if links:
        all_links.extend(links)  # Добавляем новые ссылки в общий список
    else:
        print(f"Для {date_str} новостей не найдено.")
    
    days_passed += 1 

# Оставляем только нужное количество ссылок
all_links = all_links[:links_to_collect]

# Сохраняем ссылки в файл
save_links_to_file(all_links)

print(f"Парсинг завершен. Собрано {len(all_links)} ссылок.")
