import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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


def create_graph(digits, expected, actual, mad, bar_color="silver", line_color="darkblue"):
    fig, ax = plt.subplots()
    bins = digits
    values = actual
    ax.bar(bins, values, color=bar_color, label="Actual Frequencies")
    plt.plot(digits, expected, color=line_color, label="Benford's Law Expectation")
    ax.legend()
    ax.text(x=55, y=0.035, s=f'MAD: {mad:.4f}')
    plt.xticks(np.arange(10, 91, 10))
    plt.xlim(left=9, right=99)
    plt.show()

    return fig, ax