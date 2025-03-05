import requests
from lxml import html, etree

def clean_text(text_list):
    """Функция для очистки текста: удаляет пустые строки и лишние пробелы"""
    return ' '.join([text.strip() for text in text_list if text.strip()])

def get_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)

        # Извлекаем заголовки
        title_elements = tree.xpath('//*[@id="Inhalt"]//article//header//div//h2//span//text()')
        title_elements = [t.strip() for t in title_elements if t.strip()]  # Убираем пустые строки

        short_title = title_elements[0]  # Первый элемент — краткий заголовок
        main_title = ' '.join(title_elements[1:]) # Остальное — основной заголовок

        # Краткое описание
        description_elements = tree.xpath('//*[@id="Inhalt"]//article//header//div//div//div[1]//text()')
        description = clean_text(description_elements)

        # Дата публикации
        date_elements = tree.xpath('//*[@id="Inhalt"]//article//header//div//div//div[3]//time//text()')
        date = clean_text(date_elements)

        return short_title, main_title, description, date
    else:
        print(f"Ошибка {response.status_code}: Не удалось открыть страницу")
        return None, None, None, None, None

# Проверка
url = 'https://www.spiegel.de/sport/darts-wm-2025-luke-littler-besiegt-nathan-aspinall-und-steht-im-halbfinale-a-a1d3c0a6-6e91-4090-8fc9-2946781d36f7'
short_title, main_title, description, date = get_link(url)

print(f"Краткий заголовок: {short_title}")
print(f"Основной заголовок: {main_title}")
print(f"Описание: {description}")
print(f"Дата: {date}")
