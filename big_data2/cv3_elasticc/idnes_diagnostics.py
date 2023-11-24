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

    # Query to get unique categories and their counts
    query = {
        "size": 0,
        "aggs": {
            "category_counts": {
                "terms": {
                    "field": "category",
                    "size": 10  # Set the size based on the expected number of unique categories
                    # top 10
                }
            }
        }
    }

    # Execute the query
    result = es.search(index=index_name, body=query)

    # Extract and print the category counts
    categories = result["aggregations"]["category_counts"]["buckets"]
    for category in categories:
        print(f"Category: {category['key']}, Count: {category['doc_count']}")


    # Your query to retrieve all titles
    query = {
        "_source": ["title"],
        "query": {
            "match_all": {}
        }
    }

    # Use the scroll API to retrieve all titles
    scroll_size = 1000
    response = es.search(index=index_name, body=query, scroll='2m', size=scroll_size)
    scroll_id = response['_scroll_id']

    # Extract and normalize titles, then calculate word frequencies
    word_counter = Counter()

    while len(response['hits']['hits']) > 0:
        for hit in response['hits']['hits']:
            title = hit['_source']['title'].lower()  # Normalize to lowercase
            # Tokenize the title text (you may need a more sophisticated tokenizer)
            words = title.split()
            word_counter.update(words)

        response = es.scroll(scroll_id=scroll_id, scroll='2m')

    print("Top 5 most common words in titles:")
    # Print the top 5 most common words
    for word, count in word_counter.most_common(5):
        print(f"Word: {word}, Count: {count}")


def cv2_pt2(es, index_name):
    # Query to calculate the sum of no_of_comments
    query = {
        "size": 0,
        "aggs": {
            "total_comments": {
                "sum": {
                    "field": "no_of_comments"
                }
            }
        }
    }

    # Execute the query
    result = es.search(index=index_name, body=query)

    # Extract and print the sum of no_of_comments
    total_comments = result["aggregations"]["total_comments"]["value"]
    print(f"Total Number of Comments: {total_comments}")

    # Your query to retrieve all titles and contents
    query = {
        "_source": ["title", "content"],
        "query": {
            "match_all": {}
        }
    }

    # Use the scroll API to retrieve all titles and contents
    scroll_size = 1000
    response = es.search(index=index_name, body=query, scroll='2m', size=scroll_size)
    scroll_id = response['_scroll_id']

    # Count words in titles and contents
    total_word_count = 0

    while len(response['hits']['hits']) > 0:
        for hit in response['hits']['hits']:
            # Count words in title
            title = hit['_source']['title']
            title_word_count = len(title.split())

            # Count words in content
            content = hit['_source']['content'] if 'content' in hit['_source'] else ""
            content_word_count = len(content.split())

            total_word_count += title_word_count + content_word_count

        response = es.scroll(scroll_id=scroll_id, scroll='2m')

    # Print the total word count
    print(f"Total Word Count: {total_word_count}")


def cv2_bonus(es, index_name):
    # Your query to retrieve all titles and contents
    query = {
        "_source": ["title", "content"],
        "query": {
            "match_all": {}
        }
    }

    # Use the scroll API to retrieve all titles and contents
    scroll_size = 1000
    response = es.search(index=index_name, body=query, scroll='2m', size=scroll_size)
    scroll_id = response['_scroll_id']

    # Count words with length > 6 in titles and contents
    word_counter = Counter()

    while len(response['hits']['hits']) > 0:
        for hit in response['hits']['hits']:
            # Extract and normalize titles and contents
            title = hit['_source']['title'].lower() if 'title' in hit['_source'] else ""
            content = hit['_source']['content'].lower() if 'content' in hit['_source'] else ""

            # Combine titles and contents
            combined_text = title + " " + content

            # Tokenize and count words with length > 6
            words = combined_text.split()
            long_words = [word for word in words if len(word) > 6]
            word_counter.update(long_words)

        response = es.scroll(scroll_id=scroll_id, scroll='2m')

    # Print the top 8 words with length > 6
    top_words = word_counter.most_common(8)
    for word, count in top_words:
        print(f"Word: {word}, Count: {count}")


def cv2_bonus_pt2(es, index_name):
    # Your query to retrieve the top 3 articles with the most "covid-19" occurrences
    query = {
        "_source": ["url", "title", "content"],
        "size": 3,
        "query": {
            "query_string": {
                "query": "covid-19",
                "fields": ["title", "content"]
            }
        },
        "sort": [
            {
                "_score": {
                    "order": "desc"
                }
            }
        ]
    }

    # Execute the query
    result = es.search(index=index_name, body=query)

    # just print the contents seperated by a line and the name of each of its properties
    # for hit in result['hits']['hits']:
    #     print("------------------------------------------------")
    #     print(f"URL: {hit['_source']['url']}")
    #     print(f"Title: {hit['_source']['title']}")
    #     print(f"Content: {hit['_source']['content']}")
    #     print("------------------------------------------------")

    # get the counts of "covid-19" phrases located in eachs article's title and content

    # Extract and print the counts
    for hit in result['hits']['hits']:
        title = hit['_source']['title']
        content = hit['_source']['content']

        title_count = title.lower().count("covid-19")
        content_count = content.lower().count("covid-19")

        print(f"url: {hit['_source']['url']}")
        print(f"Title Count: {title_count}, Content Count: {content_count}")

    # Your query to retrieve all content properties
    query = {
        "_source": ["url", "content"],
        "size": 1000,  # Adjust based on your dataset size
        "query": {
            "match_all": {}
        }
    }

    # Execute the query
    result = es.search(index=index_name, body=query)

    # Initialize variables for highest/lowest word count and total word length
    max_word_count = 0
    lowest_word_count = float('inf')  # Set to positive infinity initially
    max_word_count_url = ""
    total_word_count = 0

    for hit in result['hits']['hits']:
        url = hit['_source']['url']
        content = hit['_source'].get('content', '')

        # Calculate word count
        word_count = len(content.split())

        # Calculate total word length
        total_word_count += sum(len(word) for word in content.split())

        # Check if it's the highest word count so far
        if word_count > max_word_count:
            max_word_count = word_count
            max_word_count_url = url

        # Check if it's the lowest word count so far
        if word_count < lowest_word_count:
            lowest_word_count = word_count

    # Calculate average word length
    average_word_count = total_word_count / max(1, sum(1 for _ in result['hits']['hits']))

    # Print the results
    print(f"URL with Highest Word Count: {max_word_count_url}, Word Count: {max_word_count}")
    print(f"Lowest Word Count: {lowest_word_count}")
    print(f"Average Word Count: {average_word_count}")


def cv2_bonus_pt3(es, index_name):
    # Your query to retrieve all content properties
    query = {
        "_source": ["content"],
        "query": {
            "match_all": {}
        }
    }

    # Initialize variables for total word count and total word length
    total_word_count = 0
    total_word_length = 0

    # Execute the initial search using the Scroll API
    scroll_size = 1000
    response = es.search(index=index_name, body=query, scroll='2m', size=scroll_size)

    # Process the initial result
    total_word_count += sum(len(hit['_source']['content'].split()) for hit in response['hits']['hits'])
    total_word_length += sum(sum(len(word) for word in hit['_source']['content'].split()) for hit in response['hits']['hits'])

    # Continue scrolling until no more results are returned
    while len(response['hits']['hits']) > 0:
        response = es.scroll(scroll_id=response['_scroll_id'], scroll='2m')

        # Process each subsequent result
        total_word_count += sum(len(hit['_source']['content'].split()) for hit in response['hits']['hits'])
        total_word_length += sum(sum(len(word) for word in hit['_source']['content'].split()) for hit in response['hits']['hits'])

    # Calculate the average word length
    average_word_length = total_word_length / max(1, total_word_count)

    # Print the result
    print(f"Average Word Length: {average_word_length}")


def cv2_bonus_pt4(es, index_name):
    # query to retrive month with the most posts

    query = {
        "size": 0,
        "aggs": {
            "posts_per_month": {
                "date_histogram": {
                    "field": "date",
                    "calendar_interval": "month",
                    "format": "yyyy-MM",
                    "min_doc_count": 1
                }
            }
        }

    }

    result = es.search(index=index_name, body=query)

    # take the month with the most posts
    month = result["aggregations"]["posts_per_month"]["buckets"][-1]["key_as_string"]
    print(f"Month with the most posts: {month}")

    # rake the month with the least posts
    month = result["aggregations"]["posts_per_month"]["buckets"][0]["key_as_string"]
    print(f"Month with the least posts: {month}")


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
                    "size": 10  # Set a reasonable size for the terms aggregation
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
    cv2_pt2(my_elasticc, index)
    cv2_bonus(my_elasticc, index)
    cv2_bonus_pt2(my_elasticc, index)
    cv2_bonus_pt3(my_elasticc, index)
    cv2_bonus_pt4(my_elasticc, index)
    cv3(my_elasticc, index)
    cv3_pt2(my_elasticc, index)
    cv3_bonus(my_elasticc, index)


if __name__ == "__main__":
    main()
