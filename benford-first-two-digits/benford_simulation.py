import numpy as np
import pandas as pd
from utils import calculate_chi_square

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

num_trials = 1000
test_size = 1000

# Simulation loop
while is_running:

    mad_count = 0
    mad_threshold = 0.0022

    for _ in range(num_trials):
        simulated_proportions = roll_new_dataset(test_size)
        mad = measure_mad(simulated_proportions)
        if mad >= mad_threshold:
            mad_count += 1

    if mad_count / num_trials <= 0.05:
        print(f"Estimated Required Sample Size: {test_size}")
        is_running = False
    
    else:
        test_size += 50
        print(f"Sample size too small, new sample size: {test_size}")

