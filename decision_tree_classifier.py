import numpy as np
import os
import pandas as pd
import math
from queue import PriorityQueue


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

    def __init__(self):
        self.parent_node = Node()
        self.answers = None

    def fit(self, X_train, y_train):
        self.answers = y_train
        # print(f"{y_train}")
        total_possible_diseases = len(y_train.unique())
        que = PriorityQueue()
        # iterate across each symptom
        for symptom in X_train.columns:
            disease_count = len(y_train[X_train[symptom] == 1].unique())
            ig = 1 - Classifier.get_ig(disease_count, total_possible_diseases)

            que.put(ig)
        current_node = self.parent_node
        while not que.empty():
            false_child = Node(parent=current_node)
            true_child = Node()
            current_node.set_children()
            pass

    @staticmethod
    def get_ig(favorable, total_count):
        return favorable / total_count

    def predict(self, vector):
        pass
