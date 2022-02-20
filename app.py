import json
import os

import pandas as pd
from pywebio.input import *
from pywebio.output import *
from decision_tree import DecisionTree
from preprocessing import get_jaccard_sim, vocab_cleaning, spell_check


class Dataset:

    def __init__(self, data_path):
        self.symptoms = []
        self.diseases = []
        self.wiki = {}
        self.load_dataset(data_path)

    def load_dataset(self, data_path):
        data = pd.read_csv(data_path)
        self.symptoms = data.columns[1:]
        self.diseases = data['label_dis']
        self.load_wiki()

    def load_wiki(self):
        fldr = os.path.join("Data", "Wiki")
        with open(os.path.join(fldr, "diseases.json"), "r", encoding="UTF-8") as fp:
            self.wiki = json.load(fp)

    def get_user_response(self, user_symptoms):
        symptoms_vector = []
        for symptom in self.symptoms:
            symptoms_vector.append(1 if symptom in user_symptoms else 0)
            # debug_print(f"{symptom} - {symptoms_vector[symptom]}")
        return pd.DataFrame(symptoms_vector).transpose()


def display_result(response, dataset):
    print(f"reached {response}")
    folder = os.path.join("Data", "Wiki", "imgs")
    with use_scope("result", clear=True):
        if response:
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
                img = open(os.path.join(folder, wiki_info["__IMAGE_FILE__"]), 'rb').read()
                put_image(img, width='50%')
            put_table(
                info,
                header=[span(heading, col=2)])
        else:
            put_text("")




def search(resp, dataset, dt):
    search_symptoms = []
    list_of_words = list(map(str.strip, resp.split(",")))
    warnings = []
    debug_print(" got " + resp)
    for word in list_of_words:
        if word.lower() in dataset.symptoms:
            search_symptoms.append(word.lower())
        elif word != "":
            corrected_word = spell_check(word.lower())
            max_similarity, similar_word = 0, ""
            for symptom in dataset.symptoms:
                similarity = get_jaccard_sim(vocab_cleaning(corrected_word), vocab_cleaning(symptom))
                if similarity > max_similarity:
                    max_similarity = similarity
                    similar_word = symptom
            if max_similarity > 0:
                search_symptoms.append(similar_word)
            else:
                warnings.append(word)
    with use_scope("warnings", clear=True):
        if warnings:
            put_text("Warning : \n" + f"Given symptom(s) {', '.join(warnings)} not understood")

    if warnings != list_of_words:
        symptoms_vector = dataset.get_user_response(search_symptoms)
        with open("ds.txt", "w") as fp:
            fp.write(str(symptoms_vector))
        response = dt.get_diseases(symptoms_vector)
        print(response)
        display_result(response, dataset)
    else:
        display_result([], dataset)


def debug_print(s):
    with open("log.txt", "a") as fp:
        fp.write(s + "\n")


def main():
    # dt = DecisionTree(os.path.join("Data", "dis_sym_dataset_comb.csv"), "label_dis")
    dt = DecisionTree(os.path.join("Data", "preprocessed_dis_sym_comb.csv"), "label_dis")
    dt.train()
    dataset = Dataset(os.path.join("Data", "preprocessed_dis_sym_comb.csv"))
    put_scope("Result", content=put_text(""))
    put_scope("Warnings", content=put_text(""))
    print("Getting diseases")
    while True:
        resp = input("Enter comma-separated Symptoms")
        search(resp, dataset, dt)


if __name__ == '__main__':
    main()
