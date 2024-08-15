import pandas as pd
import numpy as np


def extract_first_digits(data):
    if data >= 10:
       return int(str(data)[:2])
    

def create_missing_values(full_set, partial_set):
    missing_digit_combinations = []

    for digits in full_set:
        if digits in partial_set.keys():
            continue
        else:
            missing_digit_combinations.append(digits)

    missing_proportions = np.zeros(len(missing_digit_combinations))

    return pd.Series(missing_proportions, missing_digit_combinations)