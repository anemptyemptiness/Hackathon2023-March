def find_modul_sp_sv():
    #9.	Модуль спутниковой связи

    # 	Наличие батареи
    # 	Время работы от батареи (часов)
    # 	Погрешность (м)
    import requests
    from bs4 import BeautifulSoup
    import re
    from rezDATA import Need_func

    siteURL ='https://geobox.ru'
    url_mod_sp_sviazi = 'https://geobox.ru/catalog/bpla_dlya_geodezii_i_monitoringa/aksessuary_k_bpla/oem_gps_gnss_antenny/'

    # поиск ссылок и названий модулей спутниковой связи
    name_mod_sp_sviazi, link_mod_sp_sviazi, link_img_mod_sp_sviazi = Need_func.find_link_geobox(url_mod_sp_sviazi, siteURL)

    data_modul_sp_sv = []
    ustroistvo = []
    for name in range(0, len(name_mod_sp_sviazi)):
        print(name_mod_sp_sviazi[name])
        print(link_mod_sp_sviazi[name])


        print(link_img_mod_sp_sviazi[name])
        match = re.search(r'\.[a-zA-Z]+$', link_img_mod_sp_sviazi[name]).group()
        link_img_mod_sp_sviazi[name] = link_img_mod_sp_sviazi[name].replace(match, "")
        print(link_img_mod_sp_sviazi[name])
        requestss = requests.get(link_mod_sp_sviazi[name])
        if requestss.status_code == 200:
            if 'модуль' in name_mod_sp_sviazi[name]:
                ustroistvo.append("Модуль")
            else:
                ustroistvo.append("Антенна")
            product_soup = BeautifulSoup(requestss.content, "html.parser")


            # 	Погрешность (м)
            pogr = Need_func.find_num_param(product_soup, " *[см]?м", "(точност|погрешност)")
            print(ustroistvo[name])

            # 	Наличие батареи
            have_battery= None
            text_str = product_soup.find("div", id="title").text
            text_str += product_soup.find("div", id="content").text
            if re.match(r"([батаре|аккумулятор])",text_str,re.IGNORECASE):
                have_battery = "Есть"
            #print(str(have_battery))

            # 	Время работы от батареи (часов)
            time_work_ot_bat = Need_func.find_num_param(product_soup, " (ч|мин|сек)", "(время работы от батареи|время работы)")

            data_modul_sp_sv.append({
                                'Название': name_mod_sp_sviazi[name],
                                'Ссылка': link_img_mod_sp_sviazi[name],
                                'Картинка':link_img_mod_sp_sviazi[name],
                                'Устройство': ustroistvo[name],
                                'Наличие батареи': have_battery,
                                'Время работы от батареи': time_work_ot_bat,
                                'Погрешность': pogr
                            })

    return data_modul_sp_sv

