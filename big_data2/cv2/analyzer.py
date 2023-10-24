import json
from collections import Counter
import re
from datetime import datetime
from statistics import mean


def cv2():
    # Load the JSON data
    with open('bruh.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Initialize variables
    item_count = len(data)
    title_counter = Counter(item['title'] for item in data)
    duplicate_count = sum(count - 1 for count in title_counter.values())
    oldest_item = min(data, key=lambda item: datetime.strptime(item['date_published'], '%d. %m. %Y'))
    highest_comment_item = max(data, key=lambda item: int(item['n_comments']))
    highest_picture_item = max(data, key=lambda item: int(item['image_count']))

    years_count = Counter(item['date_published'].split()[-1] for item in data)
    unique_categories = set(category for item in data for category in item['categories'])
    category_count = Counter(category for item in data for category in item['categories'])

    year_2021_words = [word for item in data if item['date_published'].endswith('2021') for word in item['content'].split()]
    common_words_2021 = [word for word, count in Counter(year_2021_words).most_common(5)]

    total_comments = sum(int(item['n_comments']) for item in data)
    total_words = sum(len(item['content'].split()) for item in data)

    print("cv2")

    # Print the results
    print(f'Item Count: {item_count}')
    print(f'Duplicate Count (Same Title): {duplicate_count}')
    print(f'Oldest Item: {oldest_item["title"]}, Published on: {oldest_item["date_published"]}')
    print(f'Item with Highest Comment Count: {highest_comment_item["title"]}, Comments: {highest_comment_item["n_comments"]}')
    print(f'Item with Highest Picture Count: {highest_picture_item["title"]}, Pictures: {highest_picture_item["image_count"]}')
    print(f'Amount of Items for Each Year:')
    for year, count in sorted(years_count.items()):
        print(f'{year}: {count}')
    print(f'Amount of Unique Categories: {len(unique_categories)}')
    print(f'Items for Each Category:')
    for category, count in category_count.items():
        print(f'{category}: {count}')
    print(f'Top 5 Most Common Words for Items from the Year 2021:')
    for word in common_words_2021:
        print(word)
    print(f'Total Amount of Comments from All Items: {total_comments}')
    print(f'Total Amount of Words from the Contents Part: {total_words}')


def cv2_bonus():

    print()
    print()
    print()
    print("cv2_bonus")

    # Load the JSON data
    with open('bruh.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Task 1: Find 8 most common words, each at least 6 characters long
    all_text = ' '.join([item['content'] for item in data])
    words = re.findall(r'\b\w{6,}\b', all_text.lower())
    common_words = [word for word, count in Counter(words).most_common(8)]
    print(f'Top 8 common words (at least 6 characters): {common_words}\n')

    # Task 2: Get top 3 items containing the most "covid-19" phrases
    # Find all items with 'covid-19' phrases
    covid_phrases = [item for item in data if re.search(r'\bcovid-19\b', json.dumps(item, ensure_ascii=False), re.I)]

    # Sort the items by the number of 'covid-19' phrases (in descending order) and store counts
    sorted_items = sorted(
        [(item, item['content'].lower().count('covid-19') + item['title'].lower().count('covid-19')) for item in covid_phrases],
        key=lambda x: x[1], reverse=True
    )[:3]

    print('Top 3 items with the most "covid-19" phrases:')
    for item, count in sorted_items:
        print(f'Title: {item["title"]}, "covid-19" Count: {count}, Word Count: {len(item["content"].split())}\n')

    # Task 3: Get the average word length across all data items
    word_lengths = [len(word) for word in words]
    average_word_length = mean(word_lengths)
    print(f'Average word length across all data items: {average_word_length}\n')

    # Task 4: Get a month with the most articles and a month with the least articles
    month_counts = Counter([item['date_published'].split('.')[1].strip() for item in data])
    most_common_month = month_counts.most_common(1)[0]
    least_common_month = month_counts.most_common()[-1]
    print(f'Month with the most articles: {most_common_month[0]}, Article Count: {most_common_month[1]}')
    print(f'Month with the least articles: {least_common_month[0]}, Article Count: {least_common_month[1]}')


if __name__ == '__main__':
    cv2()
    cv2_bonus()



