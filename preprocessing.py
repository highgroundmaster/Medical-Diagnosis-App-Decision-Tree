import numpy as np
import pandas as pd

# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Preprocessing Encoders
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder

def data_cleaning(path):
    data = pd.read_csv(path)
