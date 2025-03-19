import requests
from lxml import html, etree
import concurrent.futures
import time
import traceback

# Чистка текста
def clean_text(text_list):
    return ' '.join([text.strip() for text in text_list if text.strip()])

# Функция для получения темы и подтемы из URL
def extract_theme(url):
    parts = url.strip("/").split("/")
    theme = parts[3] if len(parts) > 3 else "Нет"
    
    # Убедимся, что подтема имеет длину менее 10 символов,
    subtheme = parts[4] if len(parts) > 4 and len(parts[4]) < 15 else "Нет"
    
    return theme, subtheme

# Функция для получения данных с сайта
def get_link(url):
    try:
        time.sleep(0.1)  # Небольшая задержка между запросами
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"Ошибка {response.status_code}: {url}")
            return None

        response.encoding = response.apparent_encoding  # Корректируем кодировку
        tree = html.fromstring(response.text)  # Парсим HTML с учетом правильной кодировки

        # Извлекаем заголовки
        title_elements = tree.xpath('//*[@id="Inhalt"]//article//header//div//h2//span//text()')
        title_elements = [t.strip() for t in title_elements if t.strip()]
        short_title = title_elements[0] if title_elements else "Нет"
        main_title = ' '.join(title_elements[1:]) if len(title_elements) > 1 else short_title

        # Краткое описание
        description_elements = tree.xpath('//*[@id="Inhalt"]//article//header//div//div//div[1]//text()')
        description = clean_text(description_elements) if description_elements else "Нет"

        # Дата публикации
        date_elements = tree.xpath('//*[@id="Inhalt"]//article//header//div//div//div[3]//time//text()')
        date = clean_text(date_elements) if date_elements else "Нет"

        # Извлекаем тему и подтему из URL
        theme, subtheme = extract_theme(url)

        return {
            "short_title": short_title,
            "main_title": main_title,
            "description": description,
            "date": date,
            "theme": theme,
            "subtheme": subtheme
        }
    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")
        print(traceback.format_exc())
        return None

# Функция для сохранения данных в XML
def save(file, new_data):
    if new_data is None:
        return

    try:
        with open(file, "ab") as f:  # Запись
            article = etree.Element("article")
            etree.SubElement(article, "theme").text = new_data["theme"]
            etree.SubElement(article, "subtheme").text = new_data["subtheme"]
            etree.SubElement(article, "short_title").text = new_data["short_title"]
            etree.SubElement(article, "main_title").text = new_data["main_title"]
            etree.SubElement(article, "description").text = new_data["description"]
            etree.SubElement(article, "date").text = new_data["date"]
            f.write(etree.tostring(article, pretty_print=True, encoding="utf-8"))  
    except Exception as e:
        print(f"Ошибка при записи в XML: {e}")
        print(traceback.format_exc())

# Функция для многопоточной обработки ссылок
def process_links(file, urls, max_threads=10):
    with concurrent.futures.ThreadPoolExecutor(max_threads) as exe:
        futures = {exe.submit(get_link, url.strip()): url for url in urls}

        for count, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            new_data = future.result()
            if new_data:
                save(file, new_data)
                print(f"[{count}] ✅ Обработана ссылка: {futures[future]}")

# Читаем ссылки из файла и запускаем обработку
with open("links.txt", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

process_links("data.xml", urls, max_threads=10)

print("🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n"
      "🟩🟩🟩 ГОТОВО 🟩🟩🟩\n"
      "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩")