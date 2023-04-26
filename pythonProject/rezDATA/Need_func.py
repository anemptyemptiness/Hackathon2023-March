import requests
from bs4 import BeautifulSoup
import re

# поиск числового параметра на страница geobox (на полях товара) по ключевому слову (на расстоянии до 30 символов)
def find_num_param(soup, reg=r'', *words):
    text_str = soup.find("div", id="title").text
    text_str += soup.find("div", id="content").text
    text_str = re.sub(r'(\s+)', ' ', text_str).lower()

    # число относящееся к word
    for word in words:
        sovpad = re.search(r'{}'.format(word) + r'\D{0,30}\d+((\.|,)\d+)?'+reg, text_str)
        if sovpad:
            numbers = sovpad.group()
            #closest_number = re.search(r'\d+((\.|,)\d+)?'+reg, numbers).group()
            #print(f'{word}: {numbers}')
            return numbers
        else:
            #print(f'Не указано: {word}')
            return None

# поиск всех товаров на странице(только на страницах) geobox
def find_link_geobox(url, siteURL):
    response = requests.get(url + "?SHOWALL_1=1")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='list-showcase__inner js-element__shadow')
        name = []
        link = []
        link_img = []
        for item in items:
            name.append(item.find('div',class_='list-showcase__name').find('a').text)
            link.append(siteURL + item.find('div',class_='list-showcase__name').find('a')['href'])
            #print(name[-1])

            allimgl = item.find('div',class_="list-showcase__picture").find('img')
            if allimgl:link_img.append(siteURL+allimgl.get("data-src"))
            else: link_img.append(None)
        return name,link,link_img
    else:
        print("ошибка запроса к сайту")

# ищем значение по регулярному значению 555 ГГц при regex = r'\d+ *ГГц'
def find_po_reg(soup, datastr, regex):
    # Ищем по страницам
    capacity_pattern = re.compile(regex)
    capacity_text = soup.find(string=capacity_pattern)
    if capacity_text:
        # извлекаем значение
        capacity_value = re.search(regex, capacity_text).group()
        #print(f"{datastr}: {capacity_value}")
        return capacity_value
    else:
        #print(f"Не найдено: {datastr}")
        return None

# из списка ["dfb","drrh","gggggg"...] ищем есть ли такие слова на всей странице
def find_mnozhestvo_po_spisku(soup,whatIsItStr, list):
    text_str = soup.find("div", id="title").text
    text_str += soup.find("div", id="content").text
    text_str = re.sub(r'(\s+)', ' ', text_str).lower()
    pattern = re.compile(r'\b(' + '|'.join(list) + r')\b', flags=re.IGNORECASE)
    matches = pattern.findall(text_str)
    if matches:
        uniq_matches = [x for i, x in enumerate(matches) if x not in matches[:i]]
        uniq_matches = ', '.join(uniq_matches)
        #print(f"{whatIsItStr}: {uniq_matches}")
        return uniq_matches
    else:
        #print(f"Не удалось найти: {whatIsItStr}")
        return None