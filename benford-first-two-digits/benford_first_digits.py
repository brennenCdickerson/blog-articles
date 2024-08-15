import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from utils import extract_first_digits, create_missing_values

# Create list of all possible first two digit combinations from 10 to 99
first_two_digits = np.arange(10, 100)

# Create list of expected Benford's Law frequencies for each first two digit combination
benford_frequencies = np.log10(1 + (1 / first_two_digits))

# Define path to target data
root_dir = Path(__file__).parent.parent
file_name = root_dir / "data" / "purchasing_card_2023.csv"

# Initial read of purchasing card transaction amounts, ignoring unused columns
purchases_df = pd.read_csv(file_name, usecols=["TRANSACTION_AMOUNT"])

# Extracts first two digits from transaction amounts
purchases_df = purchases_df.map(extract_first_digits)

# Count occurences of first two digit combinations and convert to proportion of the total count
actual_proportions = purchases_df["TRANSACTION_AMOUNT"].value_counts(normalize=True)

# If any specific first two digit combinations are missing from the data, 
# create a series with the digit combo as index and 0 as the proportion.

if len(actual_proportions < 90):
    missing_proportions = create_missing_values(first_two_digits, actual_proportions)
    complete_actual_proportions = pd.concat([actual_proportions, missing_proportions]).sort_index()

d = {"FIRST_TWO_DIGITS": first_two_digits, "EXPECTED_FREQUENCIES": benford_frequencies,
                 "ACTUAL_FREQUENCIES": complete_actual_proportions if complete_actual_proportions.any() else actual_proportions}

benford_df = pd.DataFrame(data=d)
benford_df["ABSOLUTE_DEVIATION"] = (abs(benford_df["EXPECTED_FREQUENCIES"] - benford_df["ACTUAL_FREQUENCIES"]))
mean_absolute_deviation = benford_df["ABSOLUTE_DEVIATION"].mean()



print(benford_df.head())
print(mean_absolute_deviation)
benford_df.to_csv("test.csv")


'''plt.plot(first_two_digits, benford_frequencies)
plt.xticks(np.arange(10, 91, 10))
plt.xlim(left=10)
plt.show()'''