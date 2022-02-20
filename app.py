import json
import os

import pandas as pd
from pywebio.input import *
from pywebio.output import *
from decision_tree import DecisionTree


class Dataset:

    def __init__(self):
        self.symptoms = []
        self.diseases = []
        self.wiki = {}
        self.load_dataset()

    def load_dataset(self):
        self.load_symptoms()
        self.load_diseases()
        self.load_wiki()

    def load_wiki(self):
        fldr = os.path.join("Data", "Wiki")
        with open(os.path.join(fldr, "diseases.json"), "r", encoding="UTF-8") as fp:
            self.wiki = json.load(fp)

    def load_diseases(self):
        with open(os.path.join("Data", "diseases_norm.txt"), "r", encoding="UTF-8") as fp:
            self.diseases = fp.read().splitlines()

    def load_symptoms(self):
        with open(os.path.join("Data", "symptoms.txt"), "r", encoding="UTF-8") as fp:
            self.symptoms = fp.read().splitlines()

    def get_user_response(self, user_symptoms):
        symptoms_vector = []
        for symptom in self.symptoms:
            symptoms_vector.append(1 if symptom in user_symptoms else 0)
            # debug_print(f"{symptom} - {symptoms_vector[symptom]}")
        return pd.DataFrame(symptoms_vector).transpose()


def display_result(response, dataset):
    fldr = os.path.join("Data", "Wiki", "imgs")
    with use_scope("result", clear=True):
        put_text("Your symptoms best match " + response[0])

        wiki_info = dataset.wiki[response[0]]
        heading = response[0]
        if "__HEADING__" in wiki_info.keys():
            heading = wiki_info["__HEADING__"]
        info = []
        for key in wiki_info.keys():
            if key[:2] != "__" and key[-2:] != "__":
                row = [key, wiki_info[key]]
                info.append(row)
        if "__IMAGE_FILE__" in wiki_info.keys():
            img = open(os.path.join(fldr, wiki_info["__IMAGE_FILE__"]), 'rb').read()
            put_image(img, width='50%')
        put_table(
            info,
            header=[span(heading, col=2)])



def search(resp, dataset, dt):
    search_symptoms = []
    list_of_words = list(map(str.strip, resp.split(",")))
    warnings = ""
    debug_print(" got " + resp)
    for word in list_of_words:
        if word.lower() in dataset.symptoms:
            search_symptoms.append(word)
        elif word != "":
            warnings += f"The word '{word}' was not understood\n"
    with use_scope("warnings", clear=True):
        if warnings != "":
            put_text("Warning:- \n" + warnings)
    vector = dataset.get_user_response(search_symptoms)
    with open("ds.txt", "w") as fp:
        fp.write(str(vector))
    response = dt.get_diseases(vector)
    print(response)
    display_result(response, dataset)


def debug_print(s):
    with open("log.txt", "a") as fp:
        fp.write(s + "\n")


def main():
    dt = DecisionTree(os.path.join("Data", "dis_sym_dataset_comb.csv"), "label_dis")
    dt.train()
    dataset = Dataset()
    put_scope("result", content=put_text(""))
    put_scope("warnings", content=put_text(""))
    print(" getting diseases")
    # while True:
    #     resp = input("enter symptoms separated by comma")
    #     search(resp, dataset, dt)
    for i, disease in enumerate(dataset.diseases):
        print(f" {i} of {len(dataset.diseases)}  {disease}")
        display_result([disease], dataset)
        input("next")

if __name__ == '__main__':
    main()
