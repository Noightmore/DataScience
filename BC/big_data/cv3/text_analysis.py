def analyze_text_file(filename):
    # Create empty dictionary to store letter and word counts
    letter_counts = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
    word_counts = {}

    # Read in file
    with open(filename, 'r') as f:
        text = f.read()

    # Count letter occurrences
    for letter in text:
        if letter.lower() in letter_counts:
            letter_counts[letter.lower()] += 1

    # Count word occurrences
    words = text.split()
    for word in words:
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1

    # Print letter counts
    #for letter, count in letter_counts.items():
    #    print(f"{letter}: {count}")

    # Print word counts
    # for word, count in word_counts.items():
    #    print(f"{word}: {count}")

    return letter_counts, word_counts
