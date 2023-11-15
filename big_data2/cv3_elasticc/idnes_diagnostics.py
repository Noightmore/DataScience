from collections import Counter
from datetime import datetime

from elasticsearch import Elasticsearch
import urllib3
import matplotlib.pyplot as plt


def connect():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "https"}],
                       basic_auth=('elastic', 'tDBf9G2VL=U-KmpELxYy'), verify_certs=False)

    return es


def cv2(es, index_name):
    # get count of total posts
    count = es.count(index=index_name)["count"]
    print(f"Number of posts: {count}")



    # print amount of duplicate posts urls are the same
    query = {
        "size": 0,
        "aggs": {
            "duplicate_urls": {
                "terms": {
                    "field": "url.keyword",
                    "min_doc_count": 2,
                    "size": count
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)
    print(f"Number of duplicate posts: {len(result['aggregations']['duplicate_urls']['buckets'])}")

    # get the oldest post + its url
    query = {
        "size": 1,
        "sort": [
            {
                "date": {
                    "order": "asc"
                }
            }
        ]
    }

    result = es.search(index=index_name, body=query)
    print(f"Oldest post: {result['hits']['hits'][0]['_source']['date']}")
    print(f"Oldest post url: {result['hits']['hits'][0]['_source']['url']}")


    # get the post with the highest amount of comments + its url
    query = {
        "size": 1,
        "sort": [
            {
                "no_of_comments": {
                    "order": "desc"
                }
            }
        ]
    }

    result = es.search(index=index_name, body=query)
    print(f"Post with the highest amount of comments: {result['hits']['hits'][0]['_source']['no_of_comments']}")
    print(f"Post with the highest amount of comments url: {result['hits']['hits'][0]['_source']['url']}")

    # post with the highest amount of photos + its url
    query = {
        "size": 1,
        "sort": [
            {
                "no_of_photos": {
                    "order": "desc"
                }
            }
        ]
    }

    result = es.search(index=index_name, body=query)
    print(f"Post with the highest amount of photos: {result['hits']['hits'][0]['_source']['no_of_photos']}")
    print(f"Post with the highest amount of photos url: {result['hits']['hits'][0]['_source']['url']}")


    # get the count of unique categories
    query = {
        "size": 0,
        "aggs": {
            "unique_categories": {
                "cardinality": {
                    "field": "category.keyword"
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)
    print(f"Number of unique categories: {result['aggregations']['unique_categories']['value']}")


def cv3(es, index_name):
    query = {
        "size": 0,
        "aggs": {
            "posts_per_year": {
                "date_histogram": {
                    "field": "date",
                    "calendar_interval": "year",
                    "format": "yyyy",
                    "min_doc_count": 1
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    # Extract and store the aggregation results
    aggregation_results = result["aggregations"]["posts_per_year"]["buckets"]
    years = [bucket["key_as_string"] for bucket in aggregation_results]
    doc_counts = [bucket["doc_count"] for bucket in aggregation_results]

    # Plot the data using Matplotlib with a line graph
    plt.plot(years, doc_counts, marker='o', linestyle='-', color='red')
    plt.xlabel('Year')
    plt.ylabel('Number of Posts')
    plt.title('Number of Posts per Year (Trend)')
    plt.xticks(rotation=90)  # Rotate x-axis labels
    plt.grid(True)
    plt.show()

    # Plot the data using Matplotlib
    plt.bar(years, doc_counts, color='blue')
    plt.xlabel('Year')
    plt.ylabel('Number of Posts')
    plt.title('Number of Posts per Year')
    plt.xticks(rotation=90)  # Rotate x-axis labels
    plt.show()

    # for bucket in aggregation_results:
    #     year = bucket["key_as_string"]
    #     doc_count = bucket["doc_count"]
    #     print(f"Year: {year}, Document Count: {doc_count}")

    # comment count query
    search_query = {
        "size": 10000,
        "_source": ["content", "no_of_comments"],
        "query": {
            "match_all": {}
        }
    }

    # Execute the search query
    result = es.search(index=index_name, body=search_query)

    word_count_content = []
    word_comments = []
    letter_count_dict = Counter()

    # Process the results
    for hit in result['hits']['hits']:
        content = hit['_source']['content']
        comment = hit['_source']['no_of_comments']

        # Count words in 'content' field
        word_count = len(content.split())
        word_count_content.append(word_count)
        word_comments.append(comment)

        # Count letters in each word and update the dictionary
        letter_counts = [len([char for char in word if char.isalpha()]) for word in content.split()]
        letter_count_dict.update(letter_counts)

    # plot scatter
    plt.scatter(word_comments, word_count_content, color='blue', alpha=0.5)
    plt.title('Scatter Plot of Word Count vs. Number of Comments')
    plt.xlabel('Number of Comments')
    plt.ylabel('Word Count in Content')
    plt.show()

    # plot histogram of word_count_content
    # Plotting a histogram
    plt.hist(word_count_content, bins=10, color='blue', edgecolor='black')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.title('Histogram of Word Counts in Content')
    plt.show()

    # Extract data for plotting
    letter_counts = list(letter_count_dict.keys())
    word_counts = list(letter_count_dict.values())

    # Plotting the letter counts
    plt.bar(letter_counts, word_counts)
    plt.xlabel('Letter Count')
    plt.ylabel('Number of Words')
    plt.title('Letter Counts in Words')
    plt.show()


def cv3_pt2(es, index):
    search_query = {
        "size": 0,  # To get only aggregations and not the actual documents
        "aggs": {
            "categories_count": {
                "terms": {
                    "field": "category",
                    "order": {"_key": "asc"},
                    "size": 10000  # Set a reasonable size for the terms aggregation
                }
            }
        }
    }

    # Execute the search query
    result = es.search(index=index, body=search_query)

    # Extract data for plotting
    categories = [bucket["key"] for bucket in result["aggregations"]["categories_count"]["buckets"]]
    counts = [bucket["doc_count"] for bucket in result["aggregations"]["categories_count"]["buckets"]]

    # Plotting a pie chart
    plt.pie(counts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Distribution of Items by Category")
    plt.show()

    search_query1 = {
        "_source": ["date"],
        "query": {
            "match": {
                "content": "koronavirus"
            }
        }
    }

    search_query2 = {
        "_source": ["date"],
        "query": {
            "match": {
                "content": "vakcína"
            }
        }
    }

    # Execute the search query
    result1 = es.search(index=index, body=search_query1)
    result2 = es.search(index=index, body=search_query2)

    # Assuming data1 and data2 are lists of timestamps for "koronavirus" and "vakcína"
    data1 = [hit['_source']['date'] for hit in result1['hits']['hits']]
    data2 = [hit['_source']['date'] for hit in result2['hits']['hits']]

    # Convert timestamps to years
    years1 = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").year for date in data1]
    years2 = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").year for date in data2]

    # Count occurrences for each year
    count1 = Counter(years1)
    count2 = Counter(years2)

    # Extract years and occurrences
    years1, occurrences1 = zip(*sorted(count1.items()))
    years2, occurrences2 = zip(*sorted(count2.items()))

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(years1, occurrences1, label='koronavirus', marker='o', color='blue')
    plt.plot(years2, occurrences2, label='vakcína', marker='o', color='red')

    plt.title('Occurrences of Words Over Time (Yearly Accuracy)')
    plt.xlabel('Year')
    plt.ylabel('Occurrences')
    plt.legend()
    plt.grid(True)
    plt.show()

    search_query = {
        "query": {
            "range": {
                "date": {
                    "gte": "2019-01-01T00:00:00+00:00",
                    "lt": "2020-01-01T00:00:00+00:00"
                }
            }
        }
    }

    # Execute the search query
    result = es.search(index=index, body=search_query)

    # Get the count of items
    count_of_items = result['hits']['total']['value']

    print(f"Number of items from the year 2019: {count_of_items}")

    search_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "content": "koronavirus"
                        }
                    },
                    {
                        "range": {
                            "date": {
                                "gte": "2019-01-01T00:00:00+00:00",
                                "lt": "2020-01-01T00:00:00+00:00"
                            }
                        }
                    }
                ]
            }
        }
    }

    # Execute the search query
    result = es.search(index=index, body=search_query)

    # Get the count of items
    count_of_items = result['hits']['total']['value']

    print(f"Number of items containing 'koronavirus' in the year 2019: {count_of_items}")

    search_query = {
        "size": 0,
        "aggs": {
            "posts_per_day_of_week": {
                "date_histogram": {
                    "field": "date",
                    "calendar_interval": "day",
                    "format": "EEEE",  # This format returns the full name of the day of the week
                    "min_doc_count": 1
                }
            }
        }
    }

    # Execute the search query
    result = es.search(index=index, body=search_query)

    # Extract the aggregation results
    buckets = result['aggregations']['posts_per_day_of_week']['buckets']

    day_of_week = {}
    # Print the count of items for each day of the week
    for bucket in buckets:
        day_key = bucket['key_as_string']  # key_as_string contains the formatted date
        count_of_items = bucket['doc_count']

        # Check if the day key already exists in the dictionary
        if day_key in day_of_week:
            # If it exists, add the count_of_items to the existing value
            day_of_week[day_key] += count_of_items
        else:
            # If it doesn't exist, create a new key-value pair
            day_of_week[day_key] = count_of_items

    # print(day_of_week)
    # Extract keys and values from the dictionary
    days = list(day_of_week.keys())
    counts = list(day_of_week.values())

    # Plotting the data
    plt.bar(days, counts, color='skyblue')
    plt.xlabel('Day of the Week')
    plt.xticks(rotation=90)  # Rotate x-axis labels
    plt.ylabel('Count of Items')
    plt.title('Count of Items for Each Day of the Week')
    plt.show()


def cv3_bonus(es, index_name):
    if not es.indices.exists(index=index_name):
        raise LookupError(f"Index {index_name} neexistuje")

    # random link
    query = {
        "function_score": {
            "query": {"match_all": {}},
            "random_score": {}
        }
    }

    random_link = es.search(index=index_name, query=query)["hits"]["hits"][0]["_source"]["url"]
    print(f"Random link: {random_link}")

    number_of_articles = es.count(index=index_name)["count"]
    print(f"Number of articles: {number_of_articles}")

    aggs = {
        "pocet_fotek": {
            "avg": {
                "field": "no_of_photos"
            }
        }
    }

    avg_photos = es.search(index=index_name, aggs=aggs)["aggregations"]["pocet_fotek"]["value"]
    print(f"Average number of photos: {avg_photos}")

    aggs = {
        "komentovany": {
            "range": {
                "field": "no_of_comments",
                "ranges": [
                    {"from": 100.0}
                ]
            }
        }
    }

    result = es.search(index=index_name, aggs=aggs)["aggregations"]["komentovany"]["buckets"][0]["doc_count"]
    print(f"Number of articles with more than 100 comments: {result}")

    aggs = {
        "pocet_kategorii": {
            "cardinality": {
                "field": "category"
            }
        }
    }

    unique_cats_query = es.search(index=index_name, aggs=aggs)
    no_of_uniq_cats = unique_cats_query["aggregations"]["pocet_kategorii"]["value"]

    print(f"Number of unique categories: {no_of_uniq_cats}")

    aggs = {
        "unikatni_kategorie": {
            "date_range": {
                "field": "date",
                "ranges": [
                    {
                        "from": "2022-01-01T00:00:00+00:00",
                        "to": "2022-12-01T00:00:00+00:00"
                    }
                ]
            },
            "aggs": {
                "pocet_clanku": {
                    "terms": {
                        "field": "category",
                        "size": no_of_uniq_cats
                    }
                }
            }
        }
    }

    categories_aggregation = es.search(index=index_name, aggs=aggs)["aggregations"]
    cats = []
    for bucket in categories_aggregation["unikatni_kategorie"]["buckets"][0]["pocet_clanku"]["buckets"]:
        cats.append([bucket["key"], bucket["doc_count"]])

    print("Categories in 2022:")
    for cat in cats:
        print(f"Category: {cat[0]}, number of articles: {cat[1]}")


def main():
    index = 'idnes'
    my_elasticc = connect()
    cv2(my_elasticc, index)
    #cv3(my_elasticc, index)
    # cv3_pt2(my_elasticc, index)
    #cv3_bonus(my_elasticc, index)


if __name__ == "__main__":
    main()
