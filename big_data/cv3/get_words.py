def get_top_words_by_count(d, min_word_len, number_of_words):
    # Filter out words that are too short
    d = {k: v for k, v in d.items() if len(k) >= min_word_len}

    # Sort by count in descending order
    sorted_words = sorted(d.items(), key=lambda x: x[1], reverse=True)

    # Take only the top `number_of_words` words
    top_words = dict(sorted_words[:number_of_words])

    return top_words

