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
    # we get the wikipedia homepage
    driver.get("https://www.wikipedia.org/")
    time.sleep(0.5)

    # we then enter the search term
    search_input = driver.find_element(By.ID, "searchInput")
    search_input.send_keys(search)
    search_input.send_keys(Keys.RETURN)
    # wait to allow some time for the server to respond
    time.sleep(0.5)

    # we check if the box is found else we wait for the user to correct it
    while True:
        box = driver.find_elements(By.XPATH, "//table[contains(@class, 'infobox')]")
        if len(box) == 0:
            # in the event a table is not found we wait for the user to correct the error so we can continue scraping
            print("no Table found")
            input()
            print("checking again")
        else:
            break

    return box[0]


def get_file_name(link):
    # we grab the file name from the last /
    while link.find("/") != -1:
        link = link[link.find("/") + 1:]
    return link


def get_img(link):
    output_fldr = os.path.join("Data", "Wiki", "imgs")
    driver.get("https://en.wikipedia.org" + link)
    time.sleep(0.5)
    pure_link = driver.find_element(By.XPATH, "//a[contains(@class, 'internal')]").get_attribute("href")
    print(pure_link)

    # dummy header so as not to get a 403 response
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    r = requests.get(pure_link, headers=headers)

    # response other the 200 we stop and let the user know
    # normally this means network is down
    if r.status_code != 200:
        print(f"got bad status code  {r.status_code}")
        exit()

    # we get the file name from the link
    file_name = get_file_name(pure_link)

    print(file_name)

    # we save the image file
    with open(os.path.join(output_fldr, file_name), "wb+") as fp:
        fp.write(r.content)
    return file_name


def clear(text):
    return re.sub(r"\[[0-9]\]", "", text)


def pull_data(disease_name):
    information = {}
    # grabs the box
    wikipedia_box = get_wiki_box(disease_name)
    # we use bs4 soup
    soup = BeautifulSoup(wikipedia_box.get_attribute("outerHTML"), "html5lib")

    # we find the table body
    soup = soup.find('tbody')
    # we find the rows of the table
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

    list_of_diseases = pd.read_csv(os.path.join("Data", "dis_sym_dataset_comb.csv"))["label_dis"].unique()
    scraped_data = {}
    for ele in list_of_diseases:
        if ele in scraped_data.keys():
            if len(scraped_data[ele].keys()) != 0:
                continue
        print(f"getting {ele}")
        info_box = pull_data(ele)
        scraped_data[ele] = info_box
