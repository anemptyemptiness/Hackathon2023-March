def find_pol_nagr_aeromotus():
    import requests
    import re
    from bs4 import BeautifulSoup
    from rezDATA import Need_func

    url = requests.get('https://aeromotus.ru')
    soup = BeautifulSoup(url.content, 'html.parser')

    names = []
    all_suspension_links = []
    img_suspensions_list = []


    i = 1
    vsebpla = soup.find('a', string='Все подвесы и камеры').get("href")
    all_suspension_url = requests.get(vsebpla+f'/page/{i}/')
    while all_suspension_url.status_code==200:
        all_suspension_url = requests.get(vsebpla + f"/page/{i}/")
        i += 1
        if all_suspension_url.status_code == 200:
            all_bpla_soup = BeautifulSoup(all_suspension_url.content, 'html.parser')

            info_product = all_bpla_soup.find_all("div", class_='product-inner product-item__inner')
            all_bpla = all_bpla_soup.find_all("div", class_="product-loop-body product-item__body")

            for item in info_product:
                all_suspension_links.append(
                    item.find("a", class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').get("href"))
                # ссылки на все картинки
                img_suspensions_list.append(item.find('img').get('data-src'))
                # print(img_suspensions_list[-1])
                # print(all_suspension_links[-1])


    # print(len(all_suspension_links))
    uniq_suspension_links = all_suspension_links#[x for i, x in enumerate(all_suspension_links) if x not in all_suspension_links[:i]]
    # print(len(uniq_suspension_links))
    # счетчик изображений

    pol_nagr=[]

    for i in range(0,len(uniq_suspension_links)):

        dron_response = requests.get(uniq_suspension_links[i])

        if dron_response.status_code == 200:
            product_soup = BeautifulSoup(dron_response.content, 'html.parser')
            name = product_soup.find('h1').text

            print(uniq_suspension_links[i])
            print("Название подвеса: " + name)
            match = re.search(r'\.[a-zA-Z]+$', img_suspensions_list[i]).group()
            img_suspensions_list[i] = img_suspensions_list[i].replace(match, "")
            print("Ссылка на изображение: " + img_suspensions_list[i])


            # def find_vallue_in_table(drone_soup, *iskom_strr):
            #     for iskom_str in iskom_strr:
            #         # найдем ячейку, в которой указано значение iskom_str
            #         cell = drone_soup.find(['th', 'tr'], string=re.compile(iskom_str))
            #         if cell:
            #             # получим значение из следующей за ней ячейки
            #             value = cell.find_next_sibling('td').text
            #             print(iskom_str + ": " + value)
            #             return value
            #         cell = drone_soup.find('p', string=re.compile(iskom_str))
            #         if cell:
            #             value4 = cell.text
            #             print(iskom_str + ": " + value4)
            #             return value4
            #         cell = drone_soup.find('ul', string=re.compile(iskom_str))
            #         if cell:
            #             value5 = cell.find_next_sibling('li').text
            #             print(iskom_str + ": " + value5)
            #             return value5
            #
            #     print("Не указано: " + iskom_strr[0])
            #     return None
            text_str = soup.find("div", class_="container").text
            text_str = re.sub(r'(\s+)', ' ', text_str).lower()

            def find_in_table(soup, regex, stri_naz, info_prod_text=text_str):
                daya_matr = soup.find(lambda tag: tag.name in ['th', 'td'] and re.search(regex, tag.text,
                                                                                         re.IGNORECASE))  # soup.find(["th","td",'p'], string=re.compile(regex))
                if daya_matr:
                    daya_matr = daya_matr.find_next_sibling('td')
                    if daya_matr:
                        daya_matr = daya_matr.text.strip()
                        #print(f"{stri_naz}: {daya_matr}")
                        return daya_matr
                else:
                    rezli = re.match('\s[\w ,.]*' + regex + '[\w ,.]*\s', info_prod_text, re.IGNORECASE)
                    if rezli:
                        #print(f"{stri_naz}: {rezli.group()}")
                        return rezli.group()
                    else:
                        #print(f"Не найдено: {stri_naz}")
                        return None


            # Матрица
            matrica = find_in_table(product_soup, r'[Мм]атрица', "Матрица")
            # 	Объектив
            obectiv = find_in_table(product_soup, r'Объектив', "Объектив")
            # 	Увеличение
            zoom = find_in_table(product_soup, r'([Уу]величение|[Зз]ум)', "Увеличение")
            # 	Число мегапикселей
            count_Mpixel = find_in_table(product_soup, r'(Число мегапикселей)', "Число мегапикселей")
            # 	Разрешение, TVL
            razresh = find_in_table(product_soup, r'([Рр]азрешение)', "Разрешение")
            # 	Сопровождение
            soprovozh = find_in_table(product_soup, r'(Сопровождение)', "Сопровождение")
            # 	Разрешение тепловизора
            razresh_teplovis = find_in_table(product_soup, r'([Рр]азрешение тепловизора)', "Разрешение тепловизора")
            # 	Поле зрения
            pole_zren = find_in_table(product_soup, r'(Поле зрения)', "Поле зрения")
            # 	Дальномер
            dalnometr = None
            if re.search(r'дальноме', text_str, re.IGNORECASE):
                #print("Дальномер: есть")
                dalnometr = "Есть"
            #else:
                #print("Не найдено: Дальномер")
            # 	Число осей стабилизации
            count_os_stab = find_in_table(product_soup, r'(Число осей стабилизации)', "Число осей стабилизации")
            # 	Точность
            tochnost = find_in_table(product_soup, r'(\b[Тт]очность)', "Точность")
            # 	Рабочие углы стабилизации, Тангаж
            tangazh = find_in_table(product_soup, r'(тангаж|механическ\D+диапаз)', "Рабочие углы стабилизации, Тангаж")
            # 	Рабочие углы стабилизации, Крен
            Kren = None
            kren = product_soup.find(string=re.compile(r'\bкрен\b', re.IGNORECASE))
            if kren:
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
            if re.match(r'антенна', text_str, re.IGNORECASE):
                #print("Есть Антенна")
                antenna = re.match(r'\s[\w ,.]*антенна[\w ,.]*\s', text_str, re.IGNORECASE).group()
            #else:
                #print("Не удалось найти: Антенна")
            # 	Частота (ГГц)
            regular = r'([и -,;]*\d+((\.|,)\d+)? *([ГМ]Гц))+'
            chastota = Need_func.find_po_reg(product_soup, "Частота", regular)
            # 	Число каналов
            count_canal = find_in_table(product_soup, r'(число каналов)', "Число каналов")

            pol_nagr.append({
                'Название': name,
                'Ссылка': uniq_suspension_links[i],
                'Картинка': img_suspensions_list[i],
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