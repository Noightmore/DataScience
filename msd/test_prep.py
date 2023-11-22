from scipy.stats import poisson
import numpy as np

# Set a seed for reproducibility
np.random.seed(42)

# Generate some example data with a known lambda value
true_lambda = 3.0
observations = np.random.poisson(true_lambda, size=1000)

# Calculate the MLE estimate for lambda
mle_lambda = np.mean(observations)

print("True lambda:", true_lambda)
print("MLE estimate for lambda:", mle_lambda)
