import os
import subprocess
import json
from collections import defaultdict
from datetime import datetime
from uuid import uuid4

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.util import uuid_from_time

import matplotlib.pyplot as plt

# Initialize the Cassandra cluster connection


def bonus(session):
    # basic info of size of the table
    query = (
        "SELECT * FROM system_views.disk_usage "
        "WHERE keyspace_name='news_keyspace' AND table_name='news_articles'"
    )

    res = session.execute(query)

    print(res.current_rows)

    ## Your Cassandra query to get an estimate of the total row count
    query = "SELECT COUNT(*) FROM news_keyspace.news_articles;"

    # Execute the query asynchronously
    future = session.execute_async(query)

    # Wait for the result
    result = future.result()

    # Get the count from the result
    total_row_count = result[0][0] if result else 0

    print(f"Total row count: {total_row_count}")

    # get random row
    #random_token = uuid4()

    # Retrieve a random row using the generated token
    #query = session.prepare(f"SELECT * FROM news_keyspace.news_articles WHERE token(url) >= token(?) LIMIT 1;")
    #res = session.execute(query, (random_token,))

    #print(res.current_rows)


def cv(session):

    query = f"SELECT post_date FROM news_keyspace.news_articles;"
    result = session.execute(query)
    # Extract years from the result
    years = [datetime.utcfromtimestamp(row.post_date.timestamp()).year for row in result if row.post_date]

    # Plot the graph
    plt.hist(years, bins=range(min(years), max(years) + 1), edgecolor='black', alpha=0.7)
    plt.title('Distribution of Post Dates by Year')
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.show()

    # Count the number of posts per year
    posts_per_year = defaultdict(int)
    for row in result:
        if row.post_date:
            year = datetime.utcfromtimestamp(row.post_date.timestamp()).year
            posts_per_year[year] += 1

    # Extract years and corresponding post counts
    years = list(posts_per_year.keys())
    post_counts = list(posts_per_year.values())

    # Plot the bar graph
    plt.bar(years, post_counts, color='blue')
    plt.title('Distribution of Posts Added per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Posts')
    plt.show()


def main():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('news_keyspace')

    cv(session)
    bonus(session)

    # Close the Cassandra session and cluster connection
    session.shutdown()
    cluster.shutdown()


if __name__ == '__main__':
    main()
