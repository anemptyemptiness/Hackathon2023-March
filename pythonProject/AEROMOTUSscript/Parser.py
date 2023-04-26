import re
import requests
from bs4 import BeautifulSoup

url = requests.get('https://aeromotus.ru')
soup = BeautifulSoup(url.content, 'html.parser')

img_ac_battery = [] # список ccskjr yf rfhnbyrb
pylt_links = []
name_pylt = []
link_pylt = []
i = 1
vsebpla = soup.find('a', string='Все аксессуары и запчасти').get("href")
all_pylt_url = requests.get(vsebpla+f'/page/{i}/')

while all_pylt_url.status_code==200:
    all_pylt_url = requests.get(vsebpla + f'/page/{i}/')
    i = i + 1

    if all_pylt_url.status_code == 200:
        soup = BeautifulSoup(all_pylt_url.content, "html.parser")

    for item in soup.find_all("a", {"class": "woocommerce-LoopProduct-link woocommerce-loop-product__link"}):
        title_element = item.find("h2")
        if title_element is not None and ("пульт" in title_element.text.lower()):
            name_pylt.append(title_element.text)
            link_pylt.append(item['href'])



uniq_link_pylt = [x for i, x in enumerate(link_pylt) if x not in link_pylt[:i]]
print(uniq_link_pylt)

for i in uniq_link_pylt:

    def find_vallue_in_table(pylt_soup, *iskom_strr):
        for iskom_str in iskom_strr:
            # найдем ячейку, в которой указано значение iskom_str
            cell = pylt_soup.find('td', string=re.compile(iskom_str))
            if cell is not None:
                # получим значение из следующей за ней ячейки
                value = cell.find_next_sibling('td').text
                print(iskom_str+": " + value)
                return value
            cell2 = pylt_soup.find('th', string=re.compile(iskom_str))
            if cell2 is not None:
                # получим значение из следующей за ней ячейки
                value = cell2.find_next_sibling('td').text
                print(iskom_str + ": " + value)
                return value

        print("Не указано: "+iskom_strr[0])
        return None

    pylt_response = requests.get(i)

    if pylt_response.status_code == 200:
        bpla_soup = BeautifulSoup(pylt_response.content, 'html.parser')
        name_bpla = bpla_soup.find('h1').text
        print(i)
        print(name_bpla)

        pylt_soup = BeautifulSoup(pylt_response.content, "html.parser")


        def find_mnozhestvo_po_spisku(soup, whatIsItStr, list):
            text_str = soup.find("div", class_="container").text
            text_str = re.sub(r'(\s+)', ' ', text_str).lower()
            pattern = re.compile(r'\b(' + '|'.join(list) + r')\b', flags=re.IGNORECASE)
            matches = pattern.findall(text_str)
            if matches:
                uniq_matches = [x for i, x in enumerate(matches) if x not in matches[:i]]
                uniq_matches = ', '.join(uniq_matches)
                print(f"{whatIsItStr}: {uniq_matches}")
            else:
                print(f"Не удалось найти: {whatIsItStr}")


        def find_po_reg(soup, datastr, regex):
            # Ищем по страницам
            capacity_pattern = re.compile(regex)
            capacity_text = soup.find(string=capacity_pattern)
            if capacity_text:
                # извлекаем значение
                capacity_value = re.search(regex, capacity_text).group()
                print(f"{datastr}: {capacity_value}")
                return capacity_value
            else:
                # print(f"Не найдено: {datastr}")
                return None


        regular = r'\d+((\.|,)\d+)? *([ГМ]Гц)'
        operating_frequency = find_po_reg(pylt_soup, 'Рабочая частота', regular)
        number_channels = find_vallue_in_table(pylt_soup, 'Число каналов')
        operating_current = find_vallue_in_table(pylt_soup, 'Выходная мощность', 'Мощность на выходе')
        operating_voltage = find_vallue_in_table(pylt_soup, 'Рабочее напряжение')
        transmission_power = find_vallue_in_table(pylt_soup,  'Мощность передатчика (EIRP)')
        channel_resolution = find_vallue_in_table(pylt_soup, 'Разрешение канала')
        list_bse_pr = ['Wi-Fi', 'Bluetooth', 'Zigbee', '4G/LTE', 'LORA', 'RC', 'GPS', 'Ethernet', 'Infrared', 'LoRaWAN']
        wireless_protocol = find_mnozhestvo_po_spisku(pylt_soup, 'Беспроводной протокол', list_bse_pr)





