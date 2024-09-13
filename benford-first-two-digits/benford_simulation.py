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
def measure_mad(data):
    abs_deviation = []
    keys = data.keys()

    for idx, digits in enumerate(first_two_digits):
        expected = benford_frequencies[idx]

        if digits in keys:
            actual = data.get(digits)

        else:
            actual = 0
        
        deviation = abs(actual - expected)
        abs_deviation.append(deviation)
      
    mad = np.average(abs_deviation)
    return mad

# Simulation setup
is_running = True

# Number of trials, i.e., number of synthetic distributions tested
num_trials = 2500

# Tested sample size n
n = 1000

# Critical value for mean absolute deviation
mad_threshold = 0.0022

# Acceptable false positive rate
fp_rate = 0.05

# Simulation loop
while is_running:

    mad_count = 0

    for _ in range(num_trials):
        simulated_proportions = roll_new_dataset(n)
        mad = measure_mad(simulated_proportions)
        if mad >= mad_threshold:
            mad_count += 1

    if mad_count / num_trials <= fp_rate:
        print(f"Sample Size: {n}, False positive rate: {mad_count / num_trials}")
        is_running = False

    else:
        print(f"Sample Size: {n}, False positive rate: {mad_count / num_trials}")
        n += 50
