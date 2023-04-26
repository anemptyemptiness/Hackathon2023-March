def find_bpla_aeromotus():
    import requests
    import re
    from bs4 import BeautifulSoup

    img_ac_battery = [] # список ccskjr yf rfhnbyrb
    link_ac_battery = [] # список ссылок на страницы батарей
    bpla_links = []
    url = requests.get('https://aeromotus.ru')
    soup = BeautifulSoup(url.content, 'html.parser')

    i=1
    vsebpla = soup.find('a', string='Все БПЛА').get("href")
    all_bpla_url = requests.get(vsebpla+f'/page/{i}/')
    while all_bpla_url.status_code==200:
        all_bpla_url = requests.get(vsebpla + f"/page/{i}/")
        i=i+1
        if all_bpla_url.status_code == 200:
            all_bpla_soup = BeautifulSoup(all_bpla_url.content, 'html.parser')
            info_product = all_bpla_soup.find_all("div",class_='product-inner product-item__inner')
            all_bpla = all_bpla_soup.find_all("div", class_="product-loop-body product-item__body")

            #ссылки на все БПЛА
            for item in info_product:
                bpla_links.append(item.find("a",class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').get("href"))
            #ссылки на все картинки
            #for img in all_bpla_soup.find_all('div', class_='product-thumbnail product-item__thumbnail'):
                img_ac_battery.append(item.find('img').get('data-src'))
        # else:
        #     print("error")

    #print(len(bpla_links))
    uniq_bpla_links = bpla_links#[x for i, x in enumerate(bpla_links) if x not in bpla_links[:i]]
    #print(len(img_ac_battery))
    #print(len(uniq_bpla_links))

    json_arr = []

    for i in range(0, len(uniq_bpla_links)):

        def find_vallue_in_table(drone_soup, *iskom_strr):
            for iskom_str in iskom_strr:
                # найдем ячейку, в которой указано значение iskom_str
                cell = drone_soup.find('th', string=re.compile(iskom_str))
                if cell is not None:
                    # получим значение из следующей за ней ячейки
                    value = cell.find_next_sibling('td').text
                    #print(iskom_str+": " + value)
                    return value
                cell2 = drone_soup.find('td', string=re.compile(iskom_str))
                if cell2 is not None:
                    # получим значение из следующей за ней ячейки
                    value = cell2.find_next_sibling('td').text
                    #print(iskom_str + ": " + value)
                    return value

            #print("Не указано: "+iskom_strr[0])
            return None

        dron_response = requests.get(uniq_bpla_links[i])

        if dron_response.status_code == 200:
            bpla_soup = BeautifulSoup(dron_response.content, 'html.parser')
            name_bpla = bpla_soup.find('h1').text

            print(uniq_bpla_links[i])
            print(name_bpla)

            #print(img_ac_battery[i])
            match = re.search(r'\.[a-zA-Z]+$', img_ac_battery[i]).group()
            img_ac_battery[i] = img_ac_battery[i].replace(match, "")
            print(img_ac_battery[i])

            drone_soup = BeautifulSoup(dron_response.content, "html.parser")

            max_speed = find_vallue_in_table(drone_soup, 'Макс. горизонтальная скорость',
                                             'Макс. полетная скорость \(на уровне моря, без ветра\)',
                                             'Макс. скорость \(на уровне моря в штиль\)')
            max_speed_nabora = find_vallue_in_table(drone_soup, 'Макс. скорость взлета/снижения',
                                                    'Макс. скорость набора высоты', 'Макс. скорость подъема',
                                                    'Макс. скорость при взлете')
            max_speed_snizh = find_vallue_in_table(drone_soup, 'Макс. скорость снижения',
                                                   'Макс. скорость снижения \(по вертикали\)',
                                                   'Макс. скорость вертикального снижения', 'Макс. скорость спуска',
                                                   'Макс. скорость при снижении')
            max_distanse = find_vallue_in_table(drone_soup, 'Макс. полетное расстояние', 'Макс. время полета \(без ветра\)')
            max_hight = find_vallue_in_table(drone_soup, 'Макс. высота полета над уровнем моря \(без других полезных нагрузок\)',
                                             'Макс. высота над уровнем моря', 'Макс. высота полета над уровнем моря',
                                             'Макс. потолок над уровнем моря', 'Максимальная высота взлета над уровнем моря',
                                             'Практический потолок над уровнем моря', 'Макс. высота полета',
                                             'Макс. уровень над уровнем моря    3000 м')
            energy_eat = find_vallue_in_table(drone_soup, 'энергетика', 'Энергопотребление',
                                              'Максимальное потребление энергии', 'Энергоемкость',
                                              'Энергоемкость')  # не нашла только Энергия в аккумуляторе
            massa = find_vallue_in_table(drone_soup, 'Макс. полезная нагрузка', 'Макс. взлетная масса', 'Масса',
                                         'Взлетная масса')  # масса полезной нагрузки?
            max_time_fly = find_vallue_in_table(drone_soup, 'Макс. время полета',
                                                'Макс. полетное время \(без ветра\)',
                                                'Макс. полетное время')
            count_vint = find_vallue_in_table(drone_soup,
                                              'Число винтов')

            json_arr.append({
                'Название': name_bpla,
                'Ссылка': uniq_bpla_links[i],
                'Картинка': img_ac_battery[i],
                'Максимальная скорость': max_speed,
                'Скорость набора': max_speed_nabora,
                'Скорость снижения': max_speed_snizh,
                'Максимальная дальность полета': max_distanse,
                'Максимальная высота полета': max_hight,
                'Энергопотребление': energy_eat,
                'Масса полезной погрузки': massa,
                'Продолжительность полета': max_time_fly,
                'Число винтов': count_vint
            })
    return json_arr