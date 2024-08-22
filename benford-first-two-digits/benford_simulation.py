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
num_trials = 1
origin_size = 42221
mad_threshold = 0.0019
critical_value = 1.96

# Main simulation loop

for _ in range(num_trials):
    simulated_data = roll_new_dataset(origin_size)
    mad, z = measure_conformity(simulated_data, origin_size, critical_value)
    print(mad)
    print(len(z))

    '''if mad >= origin_threshold:
        mad_count +=1'''

