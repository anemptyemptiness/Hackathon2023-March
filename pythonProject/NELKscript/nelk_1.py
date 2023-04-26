import re

import requests
from bs4 import BeautifulSoup


def single_bpla(link):
    src = requests.get(link, headers=headers).text
    bpla = BeautifulSoup(src, "html.parser")
    bpla_dict = bpla.find("h1").text
    return bpla_dict


url = "https://nelk.ru/search/?tags=&how=r&q=НЕЛК"
headers = {"Accept": "*/*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.5.708 Yowser/2.5 Safari/537.36"}
req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, "html.parser")
soup = soup.find_all("h4")
all_bpla_links = [i.find("a").get('href') for i in soup]
all_bpla_links = all_bpla_links[:5]
all_bpla_links = ["https://nelk.ru"+ i for i in all_bpla_links]

data_pult_upravl =[]
for i in all_bpla_links:
    print(i)
    name = single_bpla(i)

    def find_vallue_in_table(drone_soup, *iskom_strr):
        for iskom_str in iskom_strr:
            # найдем ячейку, в которой указано значение iskom_str
            cell = drone_soup.find('th', string=re.compile(iskom_str))
            if cell is not None:
                # получим значение из следующей за ней ячейки
                value = cell.find_next_sibling('td').text
                print(iskom_str+": " + value)
                return value
            cell2 = drone_soup.find('td', string=re.compile(iskom_str))
            if cell2 is not None:
                # получим значение из следующей за ней ячейки
                value = cell2.find_next_sibling('td').text
                print(iskom_str + ": " + value)
                return value

        print("Не указано: "+iskom_strr[0])
        return None

    dron_response = requests.get(i)

    if dron_response.status_code == 200:
        bpla_soup = BeautifulSoup(dron_response.content, 'html.parser')
        name_bpla = bpla_soup.find('h1').text

        print(i)
        print(name_bpla)

        drone_soup = BeautifulSoup(dron_response.content, "html.parser")

        max_speed = find_vallue_in_table(drone_soup, 'Макс. горизонтальная скорость',
                                         'Макс. полетная скорость \(на уровне моря, без ветра\)',
                                         'Макс. скорость \(на уровне моря в штиль\)', 'Максимальная скорость')
        max_speed_nabora = find_vallue_in_table(drone_soup, 'Макс. скорость взлета/снижения',
                                                'Макс. скорость набора высоты', 'Макс. скорость подъема',
                                                'Макс. скорость при взлете', 'Крейсерская скорость')
        max_speed_snizh = find_vallue_in_table(drone_soup, 'Макс. скорость снижения',
                                               'Макс. скорость снижения \(по вертикали\)',
                                               'Макс. скорость вертикального снижения', 'Макс. скорость спуска',
                                               'Макс. скорость при снижении', 'Крейсерская скорость')
        max_distanse = find_vallue_in_table(drone_soup, 'Макс. полетное расстояние', 'Макс. время полета \(без ветра\)')
        max_hight = find_vallue_in_table(drone_soup, 'Макс. высота полета над уровнем моря \(без других полезных нагрузок\)',
                                         'Макс. высота над уровнем моря', 'Макс. высота полета над уровнем моря',
                                         'Макс. потолок над уровнем моря', 'Максимальная высота взлета над уровнем моря',
                                         'Практический потолок над уровнем моря', 'Макс. высота полета',
                                         'Макс. уровень над уровнем моря    3000 м', 'Максимальная высота полета')
        energy_eat = find_vallue_in_table(drone_soup, 'энергетика', 'Энергопотребление',
                                          'Максимальное потребление энергии', 'Энергоемкость',
                                          'Энергоемкость')  # не нашла только Энергия в аккумуляторе
        massa = find_vallue_in_table(drone_soup, 'Макс. полезная нагрузка', 'Макс. взлетная масса', 'Масса',
                                     'Взлетная масса', 'Максимальная взлетная масса', 'Максимальная масса полезной нагрузки')  # масса полезной нагрузки?
        max_time_fly = find_vallue_in_table(drone_soup, 'Макс. время полета',
                                            'Макс. полетное время \(без ветра\)',
                                            'Макс. полетное время', 'Максимальная длительность полета',
                                            'Время полета \(в зависимости от веса полезной нагрузки\)',
                                            'Максимальное время полета')
        count_vint = find_vallue_in_table(drone_soup,
                                          'Число винтов')  # не нашла на этом сайте (но по виду у всех 4)
        data_pult_upravl.append({
            'Название': name,
            'Ссылка': all_bpla_links,
            'Максимальная скорость':max_speed,
            'Скорость набора': max_speed_nabora,
            'Скорость снижения': max_speed_snizh,
            'Максимальная дальность полета': max_distanse,
            'Максимальная высота полета': max_hight,
            'Энергопотребление': energy_eat,
            'Масса полезной погрузки': massa,
            'Продолжительность полета': max_time_fly,
            'Число винтов': count_vint
        })