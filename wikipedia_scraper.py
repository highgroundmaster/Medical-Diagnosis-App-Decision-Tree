import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import html5lib
import requests

import os
import time
import pandas as pd

driver = webdriver.Chrome()


def get_wiki_box(search):
    driver.get("https://www.wikipedia.org/")
    time.sleep(0.5)

    search_input = driver.find_element(By.ID, "searchInput")

    search_input.send_keys(search)
    search_input.send_keys(Keys.RETURN)
    time.sleep(0.5)

    while True:
        box = driver.find_elements(By.XPATH, "//table[contains(@class, 'infobox')]")
        if len(box) == 0:
            print("no item found")
            input()
            print("checking again")
        else:
            break

    return box[0]


def get_file_name(link):
    while link.find("/") != -1:
        link = link[link.find("/") + 1:]
    return link


def get_img(link):
    output_fldr = os.path.join(os.path.join("Data", "Wiki"), "imgs")
    driver.get("https://en.wikipedia.org" + link)
    time.sleep(0.5)
    pure_link = driver.find_element(By.XPATH, "//a[contains(@class, 'internal')]").get_attribute("href")
    print(pure_link)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    r = requests.get(pure_link,headers=headers)
    if r.status_code != 200:
        print(f"got bad status code  {r.status_code}")
        exit()
    file_name = get_file_name(pure_link)
    print(file_name)
    with open(os.path.join(output_fldr, file_name), "wb+") as fp:
        fp.write(r.content)
    return file_name


def clear(text):
    return re.sub(r"\[[0-9]\]", "", text)


def pull_data(disease_name):
    information = {}
    wikipedia_box = get_wiki_box(disease_name)
    soup = BeautifulSoup(wikipedia_box.get_attribute("outerHTML"), "html5lib")

    soup = soup.find('tbody')
    rows = soup.find_all('tr')
    for row in rows:
        th = row.find("th")
        td = row.find("td")
        if td is not None and len(td.select("a.image")) > 0:
            information["__IMAGE_SRC__"] = str(td.select("a.image")[0]["href"])
        elif th is not None:

            if td is not None:
                information[clear(th.get_text())] = clear(td.get_text())
            elif "__HEADING__" not in information.keys():
                information["__HEADING__"] = clear(th.get_text())
            else:
                information[th.decode_contents()] = None

    if "__IMAGE_SRC__" in information.keys():
        file_name = get_img(information["__IMAGE_SRC__"])
        information["__IMAGE_FILE__"] = file_name

    return information


def save(to_save):
    output_fldr = os.path.join("Data", "Wiki")
    with open(os.path.join(output_fldr, "diseases.json"), "w") as fp:
        json.dump(to_save, fp, indent=2)


def load():
    output_fldr = os.path.join("Data", "Wiki")
    with open(os.path.join(output_fldr, "diseases.json"), "r") as fp:
        dt = json.load(fp)
    return dt


if __name__ == '__main__':
    driver.implicitly_wait(1)
    scraped_data = load()
    list_of_d = []
    for disease in scraped_data.keys():
        atr = scraped_data[disease].keys()
        if "__IMAGE_SRC__" in atr:
            if "__IMAGE_FILE__" not in atr:
                list_of_d.append(disease)

    for i, disease in enumerate(list_of_d):
        print(f" {i} of {len(list_of_d)} {disease}")
        src = get_img(scraped_data[disease]["__IMAGE_SRC__"])
        scraped_data[disease]["__IMAGE_FILE__"] = src
        save(scraped_data)
    exit(0)

    blank_diseases = []
    for ele in scraped_data.keys():
        if len(scraped_data[ele].keys()) == 0:
            blank_diseases.append(ele)

    total = len(blank_diseases)
    for i, ele in enumerate(blank_diseases):
        print(f"disease {i} of {total} : {ele}")
        d = pull_data(ele)
        print(json.dumps(d, indent=2))
        scraped_data[ele] = d
        save(scraped_data)
    exit(0)
    list_of_diseases = pd.read_csv(os.path.join("Data", "dis_sym_dataset_comb.csv"))["label_dis"].unique()
    scraped_data = {}
    for c in list_of_diseases:
        print(c)

        d = pull_data(c)
        scraped_data[c] = d
