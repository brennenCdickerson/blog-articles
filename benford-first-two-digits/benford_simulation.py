import numpy as np
import pandas as pd

# Initial setup of an array of possible first two digit combintations and their expected frequencies according to Benford's Law
first_two_digits = np.arange(10, 100)
benford_frequencies = np.log10(1 + (1 / first_two_digits))

# Generate a set of first digit frequencies based on Benford's Law probabilities
def roll_new_dataset(size):
    rng = np.random.default_rng()
    simulated_data = pd.Series(rng.choice(first_two_digits, size, p=benford_frequencies))
    simulated_proportions = simulated_data.value_counts(normalize=True)
    return simulated_proportions

# Calculate mean absolute deviation of a single simulated dataset
def calculate_mad(data):
    abs_deviation = []
    keys = data.keys()

    for idx, digits in enumerate(first_two_digits):
        if digits in keys:
            deviation = benford_frequencies[idx] - data.get(digits)
            abs_deviation.append(abs(deviation))
        else:
            deviation = benford_frequencies[idx]
            abs_deviation.append(deviation)

    mad = np.average(abs_deviation)
    return mad

# Simulation configuration variables
count = 0
num_trials = 1000
origin_size = 5000
origin_threshold = 0.0022

# Main simulation loop

#TODO pass simulated data to calculate_mad(), increment count if threshold exceeded, test main loop AND TEST MAD FUNCTION

for _ in range(num_trials):
    simulated_data = roll_new_dataset(origin_size)
