import requests
from lxml import html

def get_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        
        header = tree.xpath('//*[@id="Inhalt"]//article//header//div//h2//span//text()')
        description = tree.xpath('//*[@id="Inhalt"]//article//header//div//div//div[1]//text()')
        date = tree.xpath('//*[@id="Inhalt"]//article//header//div//div//div[3]//time//text()')
        
        return header, description, date
    else:
        print(f"Ошибка {response.status_code}: Не удалось открыть страницу")
        return None, None, None
