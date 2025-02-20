from pyspark import SparkConf, SparkContext
import re


def clean_and_split(line):
    # Use a regular expression to split and clean the line
    words = re.split(r'[.,_*\s]+', line.lower())
    return [word for word in words if word]


def word_count():
    conf = SparkConf().setAppName("WordCount")
    sc = SparkContext(conf=conf)

    input = sc.textFile("/files/book.txt")

    # Split and clean the lines, then flatMap to a list of words
    words = input.flatMap(clean_and_split)

    # Map each word to a count of 1, then reduce by key to count occurrences
    word_counts = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)

    # Swap the key-value pairs for sorting and sort by count in descending order
    word_counts_sorted = word_counts.map(lambda x: (x[1], x[0])).sortByKey(ascending=False)

    # Take the top 20 words
    results = word_counts_sorted.take(20)

    # Print the results
    for result in results:
        count, word = result
        print(f"{word}: {count}")


if __name__ == "__main__":
    word_count()
