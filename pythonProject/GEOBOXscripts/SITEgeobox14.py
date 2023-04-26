def find_pol_nagr_geobox():
    #14.	Полезная нагрузка (подвес, который прикрепляется к коптеру)

    import requests
    from bs4 import BeautifulSoup
    import re
    from rezDATA import Need_func

    siteURL ='https://geobox.ru'
    url_podveses = 'https://geobox.ru/catalog/bpla_dlya_geodezii_i_monitoringa/aksessuary_k_bpla/aksessuary/'

    name_podves = []# список названий батарей
    link_podves = []# список ссылок на страницы батарей
    link_img_podves = []

    response = requests.get(url_podveses+'?SHOWALL_1=1')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for item in soup.find_all("div", {"class": "list-showcase__inner js-element__shadow"}):
            title_element = item.find("div", {"class": "list-showcase__name-rating"}).find("a")
            #title_element = item.find("a")
            if title_element is not None and ("подвес" in title_element.text.lower() or 'камер' in title_element.text.lower()):
                name_podves.append(title_element.text)
                link_podves.append(siteURL + title_element['href'])
                # print(name_podves[-1])
                # print(link_podves[-1])
                # name_podves.append(title_element.find('div', class_='list-showcase__name').find('a').text)
                # link_podves.append(
                #     siteURL + title_element.find('div', class_='list-showcase__name').find('a')['href'])
                allimgl = item.find('div', class_="list-showcase__picture").find('img')
                if allimgl:
                    link_img_podves.append(siteURL+allimgl.get("data-src"))
                else:
                    link_img_podves.append(None)
    else:
        print("Error")

    pol_nagr = []
    for num_item in range(0, len(link_podves)):
        response = requests.get(link_podves[num_item])
        if response.status_code==200:
            product_soup = BeautifulSoup(response.content, "html.parser")
            info_prod_text = product_soup.find("div", id="title").text + product_soup.find("div", id="content").text

            print("\n"+name_podves[num_item])
            print(link_podves[num_item])

            match = re.search(r'\.(\d|[a-zA-Z])+$', link_img_podves[num_item]).group()
            link_img_podves[num_item] = link_img_podves[num_item].replace(match, "")
            print(link_img_podves[num_item])


            def find_in_table(soup,regex,stri_naz,info_prod_text=info_prod_text):
                daya_matr = soup.find(lambda tag: tag.name in ['th', 'td'] and re.search(regex, tag.text,re.IGNORECASE))#soup.find(["th","td",'p'], string=re.compile(regex))
                if daya_matr:
                    daya_matr = daya_matr.find_next_sibling('td').text.strip()
                    #print(f"{stri_naz}: {daya_matr}")
                    return daya_matr
                else:
                    rezli = re.match('\s[\w ,.]*'+regex+'[\w ,.]*\s',info_prod_text,re.IGNORECASE)
                    if rezli:
                        #print(f"{stri_naz}: {rezli.group()}")
                        return rezli.group()
                    else:
                        #print(f"Не найдено: {stri_naz}")
                        return None


            #Матрица
            matrica = find_in_table(product_soup,r'[Мм]атрица',"Матрица")
            # 	Объектив
            obectiv = find_in_table(product_soup,r'Объектив', "Объектив")
            # 	Увеличение
            zoom = find_in_table(product_soup,r'([Уу]величение|[Зз]ум)', "Увеличение")
            # 	Число мегапикселей
            count_Mpixel = find_in_table(product_soup, r'(Число мегапикселей)', "Число мегапикселей")
            # 	Разрешение, TVL
            razresh = find_in_table(product_soup,r'([Рр]азрешение)', "Разрешение")
            # 	Сопровождение
            soprovozh = find_in_table(product_soup, r'(Сопровождение)', "Сопровождение")
            # 	Разрешение тепловизора
            razresh_teplovis = find_in_table(product_soup, r'([Рр]азрешение тепловизора)', "Разрешение тепловизора")
            # 	Поле зрения
            pole_zren = find_in_table(product_soup, r'(Поле зрения)', "Поле зрения")
            # 	Дальномер
            dalnometr = None
            if re.search(r'дальноме',info_prod_text, re.IGNORECASE):
                #print("Дальномер: есть")
                dalnometr ="Есть"
            #else:print("Не найдено: Дальномер")
            # 	Число осей стабилизации
            count_os_stab = find_in_table(product_soup, r'(Число осей стабилизации)', "Число осей стабилизации")
            # 	Точность
            tochnost = find_in_table(product_soup,r'(\b[Тт]очность)', "Точность")
            # 	Рабочие углы стабилизации, Тангаж
            tangazh = find_in_table(product_soup, r'(тангаж|механическ\D+диапаз)', "Рабочие углы стабилизации, Тангаж")
            # 	Рабочие углы стабилизации, Крен
            Kren = None
            kren = product_soup.find(string=re.compile(r'\bкрен\b',re.IGNORECASE))
            if kren :
                #print(f"Рабочие углы стабилизации, Крен: {kren}")
                Kren = kren
            else:
                Kren = find_in_table(product_soup, r'(крен|механическ\D+диапаз)', "Рабочие углы стабилизации, Крен")
            # 	Рабочие углы стабилизации, Рысканье
            rskanie = find_in_table(product_soup, r'(рысканье|механическ\D+диапаз)', "Рабочие углы стабилизации, Рысканье")
            # 	Мощность (мВт)
            mochnost = find_in_table(product_soup, r'(мощность)', "Мощность")
            # 	Питание (Вольт)
            regular = r'\d+((\.|,)\d+)? *(Вольт)'
            pitanie = Need_func.find_po_reg(product_soup, "Питание", regular)
            # 	Ток (мА)
            regular = r'\d+((\.|,)\d+)? *(мА)'
            tok = Need_func.find_po_reg(product_soup, "Ток", regular)
            # 	Антенна (при наличии указать название)
            antenna = None
            if re.match(r'антенна',info_prod_text,re.IGNORECASE):
                #print("Есть Антенна")
                antenna = re.match(r'\s[\w ,.]*антенна[\w ,.]*\s',info_prod_text,re.IGNORECASE).group()
            #else: print("Не удалось найти: Антенна")
            # 	Частота (ГГц)
            regular = r'((\d+(\.|,)\d+ *([ГМ]Гц)? *[-и,]* *)?)*\d+((\.|,)\d+)? *([ГМ]Гц)'
            chastota = Need_func.find_po_reg(product_soup, "Частота", regular)
            # 	Число каналов
            count_canal = find_in_table(product_soup, r'(число каналов)', "Число каналов")

            pol_nagr.append({
                'Название': name_podves[num_item],
                'Ссылка': link_podves[num_item],
                'Картинка': link_img_podves[num_item],
                'Матрица': matrica,
                'Объектив': obectiv,
                'Увеличение': zoom,
                'Число мегапикселей': count_Mpixel,
                'Разрешение, TVL': razresh,
                'Сопровождение': soprovozh,
                'Разрешение тепловизора': razresh_teplovis,
                'Поле зрения': pole_zren,
                'Дальномер': dalnometr,
                'Число осей стабилизации': count_os_stab,
                'Точность': tochnost,
                'Рабочие углы стабилизации, Тангаж': tangazh,
                'Рабочие углы стабилизации, Крен': Kren,
                'Рабочие углы стабилизации, Рысканье': rskanie,
                'Мощность (мВт)': mochnost,
                'Питание (Вольт)': pitanie,
                'Ток (мА)': tok,
                'Антенна': antenna,
                'Частота (ГГц)': chastota,
                'Число каналов': count_canal
            })
    return pol_nagr