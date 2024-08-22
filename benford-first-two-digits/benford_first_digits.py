import pandas as pd
import numpy as np
from pathlib import Path
from utils import extract_first_digits, create_missing_values, create_graph

# TODO: FIX - df.size picks up every row, but we know that rows < 10 are excluded from the analysis. This is going to throw off the expected count







# Create list of all possible first two digit combinations from 10 to 99
first_two_digits = np.arange(10, 100)

# Create list of expected Benford's Law frequencies for each first two digit combination
benford_frequencies = np.log10(1 + (1 / first_two_digits))

# Define path to target data. Pathlib was familiar, but if this becomes more than a proof of concept then there's no need for a library to do this.
root_dir = Path(__file__).parent.parent
file_name = root_dir / "data" / "purchasing_card_2023.csv"

# Initial read of purchasing card transaction amounts, only using financial amounts
purchases_df = pd.read_csv(file_name, usecols=["TRANSACTION_AMOUNT"])
size = purchases_df.size

# Expected Benford's Law counts
expected_counts = [i * size for i in benford_frequencies]

# Extract first two digits from transaction amounts
purchases_df = purchases_df.map(extract_first_digits)

# Count occurences of first two digit combinations and convert to a proportion of the total count
actual_counts = purchases_df["TRANSACTION_AMOUNT"].value_counts()
actual_proportions = purchases_df["TRANSACTION_AMOUNT"].value_counts(normalize=True)

# Check if any first two digit combinations are missing and fill empty amounts with zero.
if actual_proportions.size < 90:
    missing_proportions = create_missing_values(first_two_digits, actual_proportions)
    missing_counts = create_missing_values(first_two_digits, actual_counts)
    complete_actual_proportions = pd.concat([actual_proportions, missing_proportions]).sort_index()
    complete_actual_counts = pd.concat([actual_counts, missing_counts]).sort_index()
    d = {"FIRST_TWO_DIGITS": first_two_digits, "EXPECTED_COUNTS": expected_counts, "ACTUAL_COUNTS": complete_actual_counts, "EXPECTED_FREQUENCIES": benford_frequencies,
                 "ACTUAL_FREQUENCIES": complete_actual_proportions}
else:
    d = {"FIRST_TWO_DIGITS": first_two_digits, "EXPECTED_COUNTS": expected_counts, "ACTUAL_COUNTS": actual_counts.sort_index(), "EXPECTED_FREQUENCIES": benford_frequencies,
                 "ACTUAL_FREQUENCIES": actual_proportions.sort_index()}

# Create dataframe from lists / pandas series, create calculated column showing deviation from expected, calculate MAD
benford_df = pd.DataFrame(data=d)
benford_df["ABSOLUTE_DEVIATION"] = (abs(benford_df["ACTUAL_FREQUENCIES"] - benford_df["EXPECTED_FREQUENCIES"]))
benford_df["Z_STATISTIC"] = ((abs(benford_df["ACTUAL_FREQUENCIES"] - benford_df["EXPECTED_FREQUENCIES"]) - (1 / (2 * size)))
                              / np.sqrt((benford_df["EXPECTED_FREQUENCIES"] * (1 - benford_df["EXPECTED_FREQUENCIES"])) / size ))
mean_absolute_deviation = benford_df["ABSOLUTE_DEVIATION"].mean()

benford_df.to_csv("testoutputNEW.csv")

# Create graph with Benford's Law line over histogram of actual occurences
create_graph(benford_df["FIRST_TWO_DIGITS"], benford_df["EXPECTED_FREQUENCIES"], 
             benford_df["ACTUAL_FREQUENCIES"], mean_absolute_deviation)

