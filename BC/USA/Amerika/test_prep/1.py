def compute_probability():
    # Define the number of rolls and the desired sum range
    num_rolls = 10
    lower_sum = 220
    upper_sum = 270

    # Initialize a 2D array to store the probabilities
    # dp[i][j] represents the probability of achieving sum j using i rolls
    dp = [[0] * (upper_sum + 1) for _ in range(num_rolls + 1)]

    # Base case: With 0 rolls, the probability of achieving sum 0 is 1
    dp[0][0] = 1

    # Compute the probabilities using dynamic programming
    for roll in range(1, num_rolls + 1):
        for j in range(lower_sum, upper_sum + 1):
            # Calculate the probability for each possible face value
            for face in range(1, 11):
                if j - face >= 0:
                    dp[roll][j] += dp[roll - 1][j - face] / 20

    # Sum the probabilities within the desired range
    probability = sum(dp[num_rolls][lower_sum:upper_sum + 1])

    return probability

# Compute the probability
probability = compute_probability()
print(f"The probability of the sum being between 220 and 270 is approximately: {probability:.6f}")


#%%
