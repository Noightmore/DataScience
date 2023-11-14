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

    query = ("""
        SELECT
        SUBSTR(post_date, 1, 4) AS year,
        COUNT(*) AS article_count
        FROM
            news_keyspace.news_articles;
        """)

    result = session.execute(query)

    for row in result:
        print(f"Year: {row.year}, Article Count: {row.article_count}")





def main():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('news_keyspace')

    cv(session)
    #bonus(session)

    # Close the Cassandra session and cluster connection
    session.shutdown()
    cluster.shutdown()


if __name__ == '__main__':
    main()
