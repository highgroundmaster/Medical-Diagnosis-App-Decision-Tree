import random
import numpy as np
import os
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import accuracy_score


def decision_tree_sk(data):
    train, test =  data.drop("label_dis", axis=1), data["label_dis"]
    X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.3, random_state=random.randint(0, 100))
    # y_test = test["label_dis"]
    pass
if __name__ == "__main__":

    data = pd.read_csv(os.path.join("Data", "dis_sym_dataset_comb.csv"))
    print(data.sample(5))
    # decision_tree_sk(data)