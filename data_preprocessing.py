import pandas as pd
import os


def main():
    data_set = pd.read_csv(os.path.join("Data", "dis_sym_dataset_comb.csv"))
    with open(os.path.join("Data", "symptoms.txt"), "w") as fp:
        for s in data_set.columns[1:]:
            fp.write(s + "\n")
    with open(os.path.join("Data", "diseases_norm.txt"), "w", encoding="UTF-8",) as fp:

        for s in data_set["label_dis"].unique():
            fp.write(s + "\n")


if __name__ == '__main__':
    main()
