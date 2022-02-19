import random
import numpy as np
import os
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from decision_tree_classifier import Classifier

class DecisionTree:

    def __init__(self, csv_file, target_name):
        self.target_name = target_name
        self.data = None
        self.load_csv(csv_file)
        self.classifier = None

    def load_csv(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def train(self):
        train, test = self.data.drop(self.target_name, axis=1), self.data[self.target_name]
        X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.3,
                                                            random_state=random.randint(0, 100))
        # y_test = test["label_dis"]
        self.classifier = Classifier()
        self.classifier.fit(X_train, y_train)
        # y_pred = self.classifier.predict(X_test)
        # return accuracy_score(y_true=y_train, y_pred=self.classifier.predict(X_train)), accuracy_score(y_true=y_test,
        #                                                                                                y_pred=y_pred)

    def get_diseases(self, search_vector):
        return self.classifier.predict(search_vector)


if __name__ == "__main__":
    dt = DecisionTree(os.path.join("Data", "dis_sym_dataset_comb.csv"), "label_dis")
    dt.train()
    # train_score, test_score = dt.train()
    # print('Accuracy Score on train data: ', train_score)
    # print('Accuracy Score on test data: ', test_score)
