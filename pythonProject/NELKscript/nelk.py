import re

import json
import os

import requests
from bs4 import BeautifulSoup

def single_bpla(link):
    src = requests.get(link, headers=headers).text
    bpla = BeautifulSoup(src, "html.parser")
    bpla_content = bpla.find("ul", class_="tabs_content tabs-body").find_all("table", class_="colored_table")[-1]
    bpla_content = bpla_content.find_all("tr")
    bpla_dict = dict(zip([i.find("td").text.strip() for i in bpla_content[1:]], [i.find_all("td")[1].text.strip() for i in bpla_content[1:]]))
    bpla_dict["link"] = "https://nelk.ru"+bpla.find("li", id="photo-0").find("img").get("src")
    bpla_dict["Название"] = bpla.find("h1").text
    return bpla_dict


def last_bpla(link):
    src = requests.get(link, headers=headers).text
    bpla = BeautifulSoup(src, "html.parser")
    dict_bpla = {}
    bpla_content = BeautifulSoup()
    images_link = ["https://nelk.ru" + i.get("href") for i in bpla.find_all("a", class_="fancy")]
    images_link = [images_link[2], images_link[3], images_link[-2]]# 2,3, -2
    count = 0
    for i in bpla.find_all("table", class_="colored_table"):
        bpla_content = i.find_all("tr")
        i = 1
        bpla_dict = dict(
            zip([j.find("td").text.strip() for j in bpla_content[1:]], [j.find_all("td")[1].text.strip() for j in bpla_content[1:]]))
        bpla_dict["link"] = images_link[count]
        dict_bpla[bpla.find("h3", string=re.compile(f"{count+1}")).text] = bpla_dict
        count += 1
    return dict_bpla


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

mas = []
for i in all_bpla_links[:-1]:
    mas.append(single_bpla(i))
    print(single_bpla(i))
for i in last_bpla(all_bpla_links[-1]):
    mas.append(i)
mas.append(last_bpla(all_bpla_links[-1]))
print(last_bpla(all_bpla_links[-1]))

data_dir = os.path.join(os.getcwd(), 'rezDATA')
data_file = os.path.join(data_dir, 'BPLA_dji.json')
data_file = data_file.replace( "\\NELKscript" , "")
with open(data_file, "w", encoding="utf-8") as outfile:
    json.dump(mas, outfile, indent=4, ensure_ascii=False)

print("Code Complite")
