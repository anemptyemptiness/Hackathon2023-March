def find_battery_aeromotus():
    import re
    import requests
    from bs4 import BeautifulSoup
    from rezDATA import Need_func

    # URL страницы с тегом "Аккумуляторы"
    url = 'https://aeromotus.ru/product-tag/akkumulyatory/'

    # Отправляем GET-запрос на URL
    response = requests.get(url)

    battery_data = []
    # Проверяем, что запрос успешен
    if response.status_code == 200:
        # Создаем объект BeautifulSoup и передаем ему текст HTML-страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все блоки с товарами
        products = soup.find_all('li', class_='product')

        # Проходимся по каждому товару и извлекаем название, ссылку и емкость
        for product in products:
            name = product.find('h2', class_='woocommerce-loop-product__title').text.strip()
            link = product.find('a', class_='woocommerce-LoopProduct-link')['href']
            img_link = product.find("div",class_='product-thumbnail product-item__thumbnail')
            if img_link: img_link = img_link.find("img").get("data-src")
            else: img_link=None

            # Отправляем GET-запрос на страницу товара
            product_page = requests.get(link)

            # Проверяем, что запрос успешен
            if product_page.status_code == 200:
                # Создаем объект BeautifulSoup и передаем ему текст HTML-страницы товара
                product_soup = BeautifulSoup(product_page.text, 'html.parser')

                capacity_pattern = re.compile(r'\d\d\d+ *(mAh|мАч|мА/ч)')
                capacity_text = product_soup.find(string=capacity_pattern)

                print(name)
                print(link)
                if img_link:
                    match = re.search(r'\.[a-zA-Z]+$', img_link).group()
                    img_link = img_link.replace(match, "")
                print(img_link)
                capacity_pattern = re.compile(r'\d\d\d+ *(mAh|мАч|мА/ч)')
                capacity_text = soup.find(string=capacity_pattern)

                capacity_value1 = None
                if capacity_text:
                    # извлекаем значение емкости
                    capacity_value = re.search(r'\d\d\d+ *(mAh|мАч|мА/ч)', capacity_text).group()
                    capacity_value1 = re.search(r'\d\d\d+', capacity_value).group()
                    #print(f"Емкость батареи: {capacity_value1} мАч")
                    capacity_value1 = capacity_value1 + "мАч"
                #else:
                    #print("Емкость батареи не найдена")


                # тут нужно будет сделать логику на красивый и лаконичный вывод
                def find_num_param(soup, reg=r'', *words):
                    text_str = soup.text
                    text_str = re.sub(r'(\s+)', ' ', text_str).lower()

                    # число относящееся к word
                    for word in words:
                        sovpad = re.search(r'{}'.format(word) + r'\D{0,30}\d+((\.|,)\d+)?' + reg, text_str)
                        if sovpad:
                            numbers = sovpad.group()
                            # closest_number = re.search(r'\d+((\.|,)\d+)?'+reg, numbers).group()
                            #print(f'{word}: {numbers}')
                            return numbers
                        else:
                            #print(f'Не указано: {word}')
                            return None


                form_factor = None
                ed_izm = r'( *с?м?м)?'
                height = find_num_param(soup, ed_izm, 'высота')
                shir = find_num_param(soup, ed_izm, 'ширина')
                lengt = find_num_param(soup, ed_izm, 'длина')
                diam = find_num_param(soup, ed_izm, 'диаметр')
                if height is not None and shir is not None and lengt is not None:
                    form_factor = str(lengt) + "*" + str(shir) + "*" + str(height)
                elif diam is not None and height is not None:
                    form_factor = str(diam) + "*" + str(diam) + "*" + str(height)
                elif diam is not None and lengt is not None:
                    form_factor = str(lengt) + "*" + str(diam) + "*" + str(diam)
                else:
                    if height is None: height = "-"
                    if shir is None: shir = "-"
                    if lengt is None: lengt = "-"
                    form_factor = str(lengt) + "*" + str(shir) + "*" + str(height)

                razr_toka = Need_func.find_po_reg(soup, "Разряд тока", r'\d?\d(\.\d+)? *[мМ]?([Аа]мпер|A[h]^)')


                battery_data.append({
                    'Название': name,
                    'Ссылка': link,
                    'Картинка': img_link,
                    'Разряд тока': razr_toka,
                    'Емкость': capacity_value1,
                    'Форм фактор': form_factor
                })

    else:
        print('Ошибка при выполнении запроса')

    return battery_data
