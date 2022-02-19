import random
import numpy as np
import os
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import accuracy_score


def decision_tree_sk(data):
    train_data, testing_data = train_test_split(data, test_size=0.3, random_state=random.randint(0, 100))
    X_train_data = training_data.drop("Disease", axis=1)
    y_train_data = training_data["Disease"].copy()
    X_test = testing_data.drop("Disease", axis=1)
    y_test = testing_data["Disease"].copy()

if __name__ == "__main__":
    data = pd.read_csv("")