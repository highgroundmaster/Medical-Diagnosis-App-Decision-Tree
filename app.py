import os

import pandas as pd
from pywebio.input import *
from pywebio.output import *
from decision_tree import DecisionTree


class Dataset:

    def __init__(self):
        self.symptoms = []
        self.load_dataset()

    def load_dataset(self):
        self.load_symptoms()

    def load_symptoms(self):
        with open(os.path.join("Data", "symptoms.txt"), "r") as fp:
            self.symptoms = fp.read().splitlines()

    def get_user_response(self, user_symptoms):
        symptoms_vector = []
        for symptom in self.symptoms:
            symptoms_vector.append(1 if symptom in user_symptoms else 0)
            # debug_print(f"{symptom} - {symptoms_vector[symptom]}")
        return pd.DataFrame(symptoms_vector).transpose()


def display_result(response):
    with use_scope("result", clear=True):
        put_text("Congrats you have " + response[0])


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
    display_result(response)



def debug_print(s):
    with open("log.txt", "a") as fp:
        fp.write(s + "\n")


def main():
    dt = DecisionTree(os.path.join("Data", "dis_sym_dataset_comb.csv"), "label_dis")
    dt.train()
    dataset = Dataset()
    put_scope("result", content=put_text(""))
    put_scope("warnings", content=put_text(""))
    while True:
        resp = input("enter symptoms separated by comma")
        search(resp, dataset, dt)


if __name__ == '__main__':
    main()
