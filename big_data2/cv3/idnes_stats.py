import os
import subprocess
import json
from datetime import datetime

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Initialize the Cassandra cluster connection


def main():
    # SELECT * FROM system_views.disk_usage
    # WHERE keyspace_name='stackoverflow' AND table_name='baseball_stats';

    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('news_keyspace')

    query = (
        "SELECT * FROM system_views.disk_usage "
        "WHERE keyspace_name='news_keyspace' AND table_name='news_articles'"
    )

    res = session.execute(query)

    print(res.current_rows)

    # Close the Cassandra session and cluster connection
    session.shutdown()
    cluster.shutdown()


if __name__ == '__main__':
    main()
