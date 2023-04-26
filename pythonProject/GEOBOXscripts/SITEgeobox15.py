def find_pult_uprav_geobox():
    import requests
    from bs4 import BeautifulSoup
    import re
    from rezDATA import Need_func

    #15	Пульт управления (control panel)
    #url1 = 'https://geobox.ru/catalog/bpla_dlya_geodezii_i_monitoringa/aksessuary_k_bpla/pulty_upravleniya_dlya_kvadrokopterov/'

    siteURL ='https://geobox.ru'

    # Ищем все ссылки на Пульт управления (control panel)
    url_control_panel = 'https://geobox.ru/catalog/bpla_dlya_geodezii_i_monitoringa/aksessuary_k_bpla/pulty_upravleniya_dlya_kvadrokopterov/'
    name_control_panel,link_control_panel,link_img_control_panel = Need_func.find_link_geobox(url_control_panel, siteURL)
    # name_control_panel список названий батарей
    # link_control_panel список ссылок на страницы батарей

    #	Рабочая частота (ГГц)+
    # 	Число каналов
    # 	Рабочий ток (мА)
    # 	Рабочее напряжение (Вольт)
    # 	Мощность передачи (дБм)+.-
    # 	Разрешение канала
    # 	Беспроводной протокол+

    data_pult_upravl = []

    # поиск информации по пультам управления
    for i in range(0, len(link_control_panel)):
        product_page = requests.get(link_control_panel[i])

        # Проверяем, что запрос успешен
        if product_page.status_code == 200:
            product_soup = BeautifulSoup(product_page.text, 'html.parser')

            #просмотр (работа с) названия и ссылки
            print("\n" + name_control_panel[i])
            print(link_control_panel[i])

            match = re.search(r'\.(\d|[a-zA-Z])+$', link_img_control_panel[i]).group()
            link_img_control_panel[i] = link_img_control_panel[i].replace(match, "")
            print(link_img_control_panel[i])

            # 	"Число каналов"
            count_chanels = Need_func.find_num_param(product_soup, "", "[Чч]исло каналов", "[кК]аналов")
            # 	Рабочий ток (мА)
            rab_tok = Need_func.find_num_param(product_soup, "[м]А[чh]^", "[Рр]абочий ток\b", "[Сс]ила тока\b", "\b[Тт]ок[аи]?\b")

            # 	Рабочее напряжение (Вольт)
            rab_napr = Need_func.find_num_param(product_soup, "([Вв]ольт|\bВ\b)", "[Нн]апряжение", "[Рр]абочее напряжение")
            # 	Разрешение канала
            raz_can = Need_func.find_num_param(product_soup, "", "[Рр]азрешение канала")

            # print("Число каналов"+str(count_chanels))
            # print("Разрешение канала"+str(raz_can))
            # print("Рабочее напряжение (Вольт)"+str(rab_napr))
            # print("Рабочий ток (мА)"+str(rab_tok))

            # Поиск Беспроводных протоколов на странице
            list_bse_pr = ['Wi-Fi', 'Bluetooth', 'Zigbee', '4G/LTE', 'LORA', 'RC', 'GPS', 'Ethernet', 'Infrared', 'LoRaWAN']
            bes_prot = Need_func.find_mnozhestvo_po_spisku(product_soup, "Беспроводные протоколы", list_bse_pr)

            # Ищем по страницам Мощность передачи (дБм)
            regular = r'[≤=]? *\d+(\.\d+)? *(дБм|dBm)'
            mochnost = Need_func.find_po_reg(product_soup, "Мощность передачи", regular)

            # Ищем по страницам частоту
            regular = r'((\d+(\.|,)\d+ *([ГМ]Гц)? *[-и,]* *)?)*\d+((\.|,)\d+)? *([ГМ]Гц)'
            chastota = Need_func.find_po_reg(product_soup, "Рабочая частота", regular)

            data_pult_upravl.append({
                'Название': name_control_panel[i],
                'Ссылка': link_control_panel[i],
                'Картинка': link_img_control_panel[i],
                'Рабочая частота (ГГц)': chastota,
                'Число каналов': count_chanels,
                'Рабочий ток (мА)': rab_tok,
                'Рабочее напряжение (Вольт)': rab_napr,
                'Мощность передачи (дБм)': mochnost,
                'Разрешение канала': raz_can,
                'Беспроводной протокол': bes_prot
                                     })
        else:
            print("Error")
    return data_pult_upravl