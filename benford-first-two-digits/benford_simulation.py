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
    simulated_counts = simulated_data.value_counts()
    simulated_proportions = simulated_data.value_counts(normalize=True)
    return simulated_proportions, simulated_counts

# Calculate mean absolute deviation of a single simulated dataset
def measure_conformity(data, size, critical_value):
    abs_deviation = []
    z_statistics = []
    keys = data.keys()

    for idx, digits in enumerate(first_two_digits):

        expected = benford_frequencies[idx]

        if digits in keys:
            actual = data.get(digits)

        else:
            actual = 0
        
        deviation = abs(actual - expected)
        abs_deviation.append(deviation)
        z_statistic = (deviation - (1 / (2 * size))) / np.sqrt((expected * (1 - expected)) / size)

        if z_statistic >= critical_value:
            z_statistics.append(z_statistic)

    mad = np.average(abs_deviation)

    return mad, z_statistics

# Simulation configuration variables
mad_count = 0
z_count = 0
chi_count = 0
num_trials = 10000
origin_size = 210477
mad_threshold = 0.00024
critical_value = 1.96
expected_counts = [i * origin_size for i in benford_frequencies]

# Main simulation loop

for _ in range(num_trials):
    simulated_proportions, simulated_counts = roll_new_dataset(origin_size)
    mad, z = measure_conformity(simulated_proportions, origin_size, critical_value)
    chi = calculate_chi_square(simulated_counts.to_list(), expected_counts)
    print(mad)
    print(chi)
    if mad >= mad_threshold:
        mad_count += 1


print(mad_count)
