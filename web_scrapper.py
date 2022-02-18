import pickle
import re
from googlesearch import search
import warnings
import numpy as np

warnings.filterwarnings("ignore")
import requests
from bs4 import BeautifulSoup
import time


# Fetch disease list from 'www.nhp.gov.in'
# https://www.cdc.gov/diseasesconditions/az/a.html
def fetch_disease_list():
    diseases = []
    for letter in range(97, 123):
        url = f"https://www.cdc.gov/diseasesconditions/az/{chr(letter)}.html"
        # For Rate Limiting Sakes
        time.sleep(0.5)
        page = requests.get(url, verify=False)

        soup = BeautifulSoup(page.content, 'html5lib')
        all_diseases = soup.find('div', class_='az-content col')

        for element in all_diseases.find_all('a'):
            diseases.append(element.get_text().strip())

    return diseases


if __name__ == "__main__":
    diseases = fetch_disease_list()
    diseases.sort()
    diseases = np.unique(np.array(diseases))
    with open("Data/diseases.txt", 'w') as output:
        for disease in diseases:
            output.write(disease + '\n')
