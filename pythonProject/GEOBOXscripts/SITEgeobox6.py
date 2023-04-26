def find_lidar_geobox():
    # 6 Лидар

    import requests
    from bs4 import BeautifulSoup
    import re
    from rezDATA import Need_func

    siteURL ='https://geobox.ru'
    url_podveses = 'https://geobox.ru/catalog/bpla_dlya_geodezii_i_monitoringa/aksessuary_k_bpla/aksessuary/'

    name_lider = []# список названий батарей
    link_lider = []# список ссылок на страницы батарей
    link_img_lider = []

    response = requests.get(url_podveses+'?SHOWALL_1=1')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # for item in soup.find_all("div", {"class": "list-showcase__name-rating"}):
        for item in soup.find_all("div", {"class": "list-showcase__inner js-element__shadow"}):
            #title_element = item.find("a")
            title_element = item.find("div", {"class": "list-showcase__name-rating"}).find("a")
            if title_element is not None and ("лидар" in title_element.text.lower() or "лазер" in title_element.text.lower()):
                name_lider.append(title_element.text)
                link_lider.append(siteURL + title_element['href'])
                # print(name_ac_battery[-1])
                allimgl = item.find('div', class_="list-showcase__picture").find('img')
                if allimgl:
                    link_img_lider.append(siteURL + allimgl.get("data-src"))
                else:
                    link_img_lider.append(None)
                # print(name_lider[-1])
                # print(link_lider[-1])
                # print(link_img_lider[-1])
    else:
        print("Error")

    data_lidar = []

    for n in range(0,len(link_lider)):
        product_page = requests.get(link_lider[n])

        # Проверяем, что запрос успешен
        if product_page.status_code == 200:
            product_soup = BeautifulSoup(product_page.content,"html.parser")

            print(name_lider[n])
            print(link_lider[n])

            #print(link_img_lider[n])
            match = re.search(r'\.[a-zA-Z]+$', link_img_lider[n]).group()
            link_img_lider[n] = link_img_lider[n].replace(match, "")
            print(link_img_lider[n])

            # 	Максимальная дальность использования (метров)
            dalnost = Need_func.find_num_param(product_soup, r" *[скм]?м", "максимальная дальность|дальность|дистанция")
            # 	Частота импульсов (Герц)
            regular = r'((\d+(\.|,)\d+ *([ГМк]Гц)? *[-и,]* *)?)*\d+((\.|,)\d+)? *([ГМкм]?Гц)'
            chastota = Need_func.find_po_reg(product_soup, "Рабочая частота", regular)
            # 	Питание (вольт)
            pitanie = Need_func.find_po_reg(product_soup, "Рабочая частота", r'\d+(\.\d+)? *(V\b|Вольт)')

            data_lidar.append({'Название': name_lider[n],
                               'Ссылка': link_lider[n],
                               'Картинка': link_img_lider[n],
                               'Максимальная дальность использования': dalnost,
                               'Частота импульсов': chastota,
                               'Питание': pitanie
                                })
    return data_lidar
