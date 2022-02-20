import random

import numpy as np
import os
import pandas as pd
import math
from queue import PriorityQueue

from sklearn.model_selection import train_test_split


class Node:

    def __init__(self, parent=None):
        self.parent = parent
        if self.parent is None:
            self.parent = self
        self.true_child = None
        self.false_child = None
        self.is_leaf_node = True
        self.symptom = None
        self.disease = ""

    def set_parent(self, node):
        self.parent = node

    def set_children(self, true_child, false_child, symptom):
        self.true_child = true_child
        self.false_child = false_child
        self.symptom = symptom
        self.is_leaf_node = False

    def set_disease(self, disease):
        self.disease = disease


class Classifier:

    def __init__(self, comb_csv, norm_csv, target_name="label_dis"):
        self.parent_node = Node()
        self.data = None
        self.data_unique = None
        self.target = target_name
        self.load_data(comb_csv, norm_csv)
        self.X_train = None
        self.y_train = None
        self.y_test = None
        self.X_test = None

    def load_data(self, comb_csv, norm_csv):
        self.data = pd.read_csv(comb_csv)
        self.data_unique = pd.read_csv(norm_csv)

    def fit(self):
        train, test = self.data.drop(self.target, axis=1), self.data[self.target]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(train, test, test_size=0.3,
                                                                      random_state=random.randint(0, 100))

        # print(f"{y_train}")
        total_possible_diseases = len(self.y_train.unique())
        entropy_queue = PriorityQueue()
        # iterate across each symptom
        for symptom in self.X_train.columns:
            entropy = self.get_entropy(symptom)
            print(f"{symptom} - {entropy}")
            # ig = 1 - Classifier.get_ig(disease_count, total_possible_diseases)

        #     entropy_queue.put(ig)
        # current_node = self.parent_node
        # while not entropy_queue.empty():
        #     false_child = Node(parent=current_node)
        #     true_child = Node()
        #     current_node.set_children()
        #     pass

    def get_entropy(self, symptom):
        diseases = self.y_train.unique()
        total_possible_diseases = len(diseases)
        entropy, sum_1 = 0, 0
        # Each Disease Probability
        for disease in diseases:
            count_1 = int(True in (self.X_train[symptom] == 1) & (self.y_train == disease))
            sum_1 += count_1
            entropy -= math.log(count_1 / total_possible_diseases, 2) * count_1 / total_possible_diseases

        # No disease Probability
        count_0 = total_possible_diseases - sum_1
        return entropy - math.log(count_0 / total_possible_diseases, 2) * count_0 / total_possible_diseases

    @staticmethod
    def get_ig(favorable, total_count):
        return favorable / total_count

    def predict(self, vector):
        pass
