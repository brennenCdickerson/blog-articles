import numpy as np
import pandas as pd

# Initial setup of an array of possible first two digit combintations and their expected frequencies according to Benford's Law.
first_two_digits = np.arange(10, 100)
benford_frequencies = np.log10(1 + (1 / first_two_digits))

rng = np.random.default_rng()
simulated_data = pd.Series(rng.choice(first_two_digits, 5000, p=benford_frequencies))

simulated_proportions = simulated_data.value_counts(normalize=True)



abs_deviation = []
keys = simulated_proportions.keys()


'''for idx, digits in enumerate(first_two_digits):
    if digits in keys:
        deviation = benford_frequencies[idx] - simulated_proportions.get(digits)'''

