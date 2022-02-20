import os.path

import numpy as np
import pandas as pd
import nltk


nltk.download("wordnet")
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt')

from itertools import combinations

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet


def data_cleaning():
    data = pd.read_csv(os.path.join("Data", "preprocessed_dis_sym_comb.csv"))
    symptoms = data.columns[1:]
    for symptom_1, symptom_2 in list(combinations(symptoms, 2)):
        if get_jaccard_sim(vocab_cleaning(symptom_1),vocab_cleaning(symptom_2)) >= 0.5:
            choice = int(input(f" 1. {symptom_1}\n 2. {symptom_2}\n 3. Name Change \n 4. Pass\n\n"))
            if choice < 3:
                data["temp"] = data[[symptom_1, symptom_2]].max(axis=1)
                name = symptom_1 if choice == 1 else symptom_2
                data = data.drop(columns=[symptom_1, symptom_2])
                data[name] = data["temp"]
            elif choice == 3:
                name = input("Enter the Column Name :")
                data[name] = data[[symptom_1, symptom_2]].max(axis=1)
                data = data.drop(columns=[symptom_1, symptom_2])
            else:
                pass
    data = data.drop(columns="temp")
    data = data[sorted(data.columns)]
    data.to_csv("..\preprocessed_comb.csv")


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def vocab_cleaning(sentence):
    # Remove Stop Words
    stop_words = set(stopwords.words('english'))
    stop = " ".join([token for token in sentence.split() if token not in stop_words])

    # tokenize the sentence and find the POS tag for each token
    pos_tagged = nltk.pos_tag(nltk.word_tokenize(stop))
    # we use our own pos_tagger function to make things simpler to understand.
    pos_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

    # Init Lemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []

    for word, tag in pos_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    # print(a, b)
    return len(c) / (len(a) + len(b) - len(c))
