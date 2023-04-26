def fnd_battery_geobox():
    import requests
    from bs4 import BeautifulSoup
    import re
    from rezDATA import Need_func

    siteURL ='https://geobox.ru'
    url_ac_battery = 'https://geobox.ru/catalog/77-prinadlezhnosti/47-akkumulyatory/'
    # name_ac_battery # список названий батарей
    # link_ac_battery # список ссылок на страницы батарей

    # поиск ссылок и названий батарей и аккумуляторов
    name_ac_battery, link_ac_battery, link_img_ac_battery = Need_func.find_link_geobox(url_ac_battery, siteURL)


    #это ссылка на аккумуляторы и зарядки для БПЛА (отсеиваем то что нам нужно)
    url_ac_battery_bpla = 'https://geobox.ru/catalog/bpla_dlya_geodezii_i_monitoringa/aksessuary_k_bpla/zaryadnye_ustroystva_i_akkumulyatory/?SHOWALL_1=1'
    response = requests.get(url_ac_battery_bpla)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for item in soup.find_all("div", {"class": "list-showcase__inner js-element__shadow"}):

            #for item in soup.find_all("div", {"class": "list-showcase__name-rating"}):

            title_element = item.find("div", {"class": "list-showcase__name-rating"}).find("a")
            if title_element is not None and (
                    "аккумулятор" in title_element.text.lower() or
                    "батаре" in title_element.text.lower()) and not \
                    "заряд" in title_element.text.lower():
                if not title_element.text in name_ac_battery:
                    # name_ac_battery.append(title_element.find('div', class_='list-showcase__name').find('a').text)
                    # link_ac_battery.append(siteURL + title_element.find('div', class_='list-showcase__name').find('a')['href'])
                    name_ac_battery.append(title_element.text)
                    link_ac_battery.append(siteURL+title_element['href'])
                    #print(name_ac_battery[-1])
                    allimgl = item.find('div', class_="list-showcase__picture").find('img')
                    if allimgl:
                        link_img_ac_battery.append(siteURL + allimgl.get("data-src"))
                    else:
                        link_img_ac_battery.append(None)
    else:
        print("Error")



    # 	Разряд тока (Ампер);
    # 	Емкость (мА/ч);
    # 	Форм фактор (длина * ширина * высота)

    battery_data=[]
    #print(len(link_ac_battery))
    # поиск информации по батареям и аккумуляторам
    for i in range(0, len(link_ac_battery)):
        product_page = requests.get(link_ac_battery[i])

        # Проверяем, что запрос успешен
        if product_page.status_code == 200:
            # Создаем объект BeautifulSoup и передаем ему текст HTML-страницы товара
            product_soup = BeautifulSoup(product_page.text, 'html.parser')

            print("\n"+name_ac_battery[i])
            print(link_ac_battery[i])

            #print(link_img_ac_battery[i])
            match = re.search(r'\.[a-zA-Z]+$', link_img_ac_battery[i]).group()
            link_img_ac_battery[i] = link_img_ac_battery[i].replace(match,"")
            print(link_img_ac_battery[i])

            form_factor=None
            #razr_toka=None
            Iemkost = None
            # Разряд тока(Ампер) нет и на одной странице, без понятия какая должна быть маска
            razr_toka = Need_func.find_po_reg(product_soup, "Разряд тока", r'\d?\d(\.\d+)? *[мМ]?([Аа]мпер|A[h]^)')

            #тут нужно будет сделать логику на красивый и лаконичный вывод
            ed_izm = r'( *с?м?м)?'
            height = Need_func.find_num_param(product_soup, ed_izm, 'высота')
            shir = Need_func.find_num_param(product_soup, ed_izm, 'ширина')
            lengt = Need_func.find_num_param(product_soup, ed_izm, 'длина')
            diam = Need_func.find_num_param(product_soup, ed_izm, 'диаметр')
            if height is not None and shir is not None and lengt is not None:
                form_factor = str(lengt)+"*"+str(shir)+"*"+str(height)
            elif diam is not None and height is not None:
                form_factor = str(diam)+"*"+str(diam)+"*"+str(height)
            elif diam is not None and lengt is not None:
                form_factor = str(lengt) + "*" + str(diam) + "*" + str(diam)
            else:
                if height is None: height="-"
                if shir is None: shir="-"
                if lengt is None: lengt="-"
                form_factor = str(lengt)+"*"+str(shir)+"*"+str(height)


            # Ищем по страницам емкость батареи
            capacity_pattern = re.compile(r'\d\d\d+ *(mAh|мАч|мА/ч)')
            capacity_text = product_soup.find(string=capacity_pattern)

            if capacity_text:
                # извлекаем значение емкости
                capacity_value = re.search(r'\d *\d\d+ *(mAh|мАч|мА/ч)', capacity_text).group()
                capacity_value1 = re.search(r'\d *\d\d+', capacity_value).group()
                #print(f"Емкость батареи: {capacity_value1} мАч")
                Iemkost = f"{capacity_value1} мАч"
            else:
                capacity_pattern = re.compile(r'\d+((\.|,)\d+)? *(Ач|Ah)')
                capacity_text = product_soup.find(string=capacity_pattern)
                if capacity_text:
                    # извлекаем значение емкости
                    capacity_value = re.search(r'\d+((\.|,)\d+)? *(Ач|Ah)', capacity_text).group()
                    capacity_value1 = re.search(r'\d+((\.|,)\d+)?', capacity_value).group()
                    num_float = float(capacity_value1.replace(',', '.'))
                    #print(f"Емкость батареи: {float(num_float)*1000} мАч")
                    Iemkost = f"{float(num_float)*1000} мАч"
                else:
                    #print("Емкость батареи не найдена")
                    Iemkost = None

            battery_data.append({
                            'Название': name_ac_battery[i],
                            'Ссылка': link_ac_battery[i],
                            'Картинка':link_img_ac_battery[i],
                            'Разряд тока': razr_toka,
                            'Емкость': Iemkost,
                            'Форм фактор': form_factor
                        })
        else:
            print("Error")
    return battery_data
