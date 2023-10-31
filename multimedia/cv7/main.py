import numpy as np


def normalize_probabilities(probs):
    total_prob = sum(probs.values())
    normalized_probs = {k: v / total_prob for k, v in probs.items()}
    return normalized_probs


def calculate_cumulative_probabilities(probs):
    cumulative_probs = {}
    cumulative_prob = 0.0
    for symbol, prob in sorted(probs.items()):
        cumulative_prob += prob
        cumulative_probs[symbol] = cumulative_prob
    return cumulative_probs


def arithmetic_encode(message, probs):
    normalized_probs = normalize_probabilities(probs)
    cumulative_probs = calculate_cumulative_probabilities(normalized_probs)

    low = 0.0
    high = 1.0

    for symbol in message:
        range_size = high - low
        high = low + range_size * cumulative_probs[symbol]
        low = low + range_size * (cumulative_probs[symbol] - probs[symbol])

    return (low + high) / 2


def arithmetic_decode(encoded_val, probs, message_length):
    normalized_probs = normalize_probabilities(probs)
    cumulative_probs = calculate_cumulative_probabilities(normalized_probs)

    message = []
    low = 0.0
    high = 1.0

    for _ in range(message_length):
        for symbol, cumulative_prob in sorted(cumulative_probs.items(), key=lambda x: x[1]):
            symbol_low = low + (high - low) * (cumulative_prob - probs[symbol])
            symbol_high = low + (high - low) * cumulative_prob

            if symbol_low <= encoded_val < symbol_high:
                message.append(symbol)
                high = symbol_high
                low = symbol_low
                break

    return np.array(message)


if __name__ == '__main__':
    with open('Cv07_Aritm_data.bin', 'r', encoding="utf-8") as f:
        nums = np.fromfile(f, dtype='uint8')

    print(f"nums: {nums}")

    unique, counts = np.unique(nums, return_counts=True)
    probabilities = dict(zip(unique, counts / len(nums)))

    print(f"probabilities: {probabilities}")

    encoded_value = arithmetic_encode(nums, probabilities)
    print(f"encoded_value: {encoded_value}")

    decoded_value = arithmetic_decode(encoded_value, probabilities, len(nums))
    print(f"decoded_value: {decoded_value}")
