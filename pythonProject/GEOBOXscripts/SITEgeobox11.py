def find_teplovis_geobox():
    #11.	Тепловизор

    import requests
    from bs4 import BeautifulSoup
    import re
    from rezDATA import Need_func

    siteURL ='https://geobox.ru'
    url_podveses = 'https://geobox.ru/catalog/bpla_dlya_geodezii_i_monitoringa/aksessuary_k_bpla/aksessuary/'

    name_teplovisor = []# список названий батарей
    link_teplovisor = []# список ссылок на страницы батарей
    link_img_teplovisor = []

    response = requests.get(url_podveses+'?SHOWALL_1=1')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for item in soup.find_all("div", {"class": "list-showcase__inner js-element__shadow"}):
            title_element = item.find("div", {"class": "list-showcase__name-rating"}).find("a")
            #title_element = item.find("a")
            if title_element is not None and "тепловиз" in title_element.text.lower():
                name_teplovisor.append(title_element.text)
                link_teplovisor.append(siteURL + title_element['href'])
                #print(name_teplovisor[-1])
                # name_teplovisor.append(title_element.find('div', class_='list-showcase__name').find('a').text)
                # link_teplovisor.append(
                #     siteURL + title_element.find('div', class_='list-showcase__name').find('a')['href'])
                allimgl = item.find('div', class_="list-showcase__picture").find('img')
                if allimgl:
                    link_img_teplovisor.append(siteURL+allimgl.get("data-src"))
                else:
                    link_img_teplovisor.append(None)
    else:
        print("Error")

    data_teplovis =[]
    for n in range(0,len(link_teplovisor)):
        response = requests.get(link_teplovisor[n])
        if response.status_code == 200:
            product_soup = BeautifulSoup(response.content,"html.parser")
            info_prod_text = product_soup.find("div", id="title").text + product_soup.find("div", id="content").text

            print("\n"+name_teplovisor[n])
            print(link_teplovisor[n])

            match = re.search(r'\.(\d|[a-zA-Z])+$', link_img_teplovisor[n]).group()
            link_img_teplovisor[n] = link_img_teplovisor[n].replace(match, "")
            print(link_img_teplovisor[n])

            def find_in_table(soup, regex, stri_naz, info_prod_text=info_prod_text):
                daya_matr = soup.find(lambda tag: tag.name in ['th', 'td'] and re.search(regex, tag.text,
                                                                                         re.IGNORECASE))  # soup.find(["th","td",'p'], string=re.compile(regex))
                if daya_matr:
                    daya_matr = daya_matr.find_next_sibling('td').text.strip()
                    print(f"{stri_naz}: {daya_matr}")
                    return daya_matr
                else:
                    rezli = re.match('\s[\w ,.]*' + regex + '[\w ,.]*\s', info_prod_text, re.IGNORECASE)
                    if rezli:
                        print(f"{stri_naz}: {rezli.group()}")
                        return rezli.group()
                    else:
                        print(f"Не найдено: {stri_naz}")
                        return None

            # 	Дальность обнаружения (м)
            dal_obn = Need_func.find_num_param(product_soup, "к?м", "(дальность обнаруж|обнаруж)")
            # 	Дистанция наблюдения (м)
            dist_nab = Need_func.find_num_param(product_soup, "к?м", "(дистанция наблюдения|наблюдени)")
            # 	Интерфейс
            interf = find_in_table(product_soup, r'([Ии]нтерфейс)', "Интерфейс")
            # 	Напряжение (Вольт)
            naprazh = Need_func.find_po_reg(product_soup, "Напряжение", "(Вольт|\bВ\b)")
            # 	Наличие батареи (Вт/ч)
            batary = None
            if re.search(r'батаре', info_prod_text, re.IGNORECASE):
                print("Батарея: есть")
                batary = "Есть"
            else:
                print("Не найдено: Батарея")
            # 	Время работы от батареи (ч)
            time_bat = Need_func.find_num_param(product_soup, "[чм]", "(Время работы от батареи|автономно)")
            # 	Поле зрения
            pole_zren = find_in_table(product_soup, r'(Поле зрения)', "Поле зрения")
            # 	Увеличение (кратность, например: 2x, 3x, 4x)
            zoom = find_in_table(product_soup, r'([Уу]величение|[Зз]ум)', "Увеличение")
            # 	Класс защиты
            class_def = Need_func.find_num_param(product_soup, "", "класс защиты")
            # 	Рабочая температура
            rab_temp = find_in_table(product_soup, r'рабоч\D+ температур', "Рабочая температура")
            # 	Тип матрицы
            matrica = find_in_table(product_soup, r'[Мм]атрица', "Матрица")

            data_teplovis.append({
                'Название': name_teplovisor[n],
                'Ссылка': link_teplovisor[n],
                'Картинка': link_img_teplovisor[n],
                'Дальность обнаружения': dal_obn,
                'Дистанция наблюдения': dist_nab,
                'Интерфейс': interf,
                'Напряжение (Вольт)': naprazh,
                'Наличие батареи': batary,
                'Время работы от батареи': time_bat,
                'Поле зрения': time_bat,
                'Увеличение': zoom,
                'Класс защиты': class_def,
                'Рабочая температура': rab_temp,
                'Тип матрицы': matrica
            })
        else:
            print("Error")
    return data_teplovis