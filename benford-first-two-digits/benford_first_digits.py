import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

first_two_digits = np.arange(10, 100)
benford_frequencies = np.log10(1 + (1 / first_two_digits))

plt.plot(first_two_digits, benford_frequencies)
plt.xticks(np.arange(10, 91, 10))
plt.xlim(left=10)
plt.show()