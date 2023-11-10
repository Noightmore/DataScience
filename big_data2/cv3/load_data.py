import os
import json
from datetime import datetime

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Initialize the Cassandra cluster connection
cluster = Cluster(['172.17.0.2'])  # Replace with your Cassandra cluster's address
session = cluster.connect('news_keyspace')  # Replace with your keyspace

drop_table_query = "DROP TABLE IF EXISTS news_articles;"

# Execute the drop table query
#session.execute(drop_table_query)


# Define the table creation query
table_creation_query = (
    "CREATE TABLE IF NOT EXISTS news_articles ("
    "    url TEXT PRIMARY KEY,"
    "    title TEXT,"
    "    category TEXT,"
    "    content TEXT,"
    "    no_of_photos INT,"
    "    post_date TIMESTAMP,"
    "    no_of_comments INT"
    ");"
)

# Execute the table creation query
session.execute(table_creation_query)


# Folder containing JSON files
json_folder = '/home/rob/Programming/DataScience/big_data2/data'

# Iterate through JSON files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        with open(os.path.join(json_folder, filename), 'r') as json_file:
            data = json.load(json_file)

            # Iterate through JSON object keys (which are URLs)
            for url, json_obj in data.items():
                # Extract values from JSON object
                title = json_obj['title']
                category = json_obj['category']
                content = json_obj['content']
                no_of_photos = int(json_obj['no_of_photos'])
                date = json_obj['date']
                no_of_comments = int(json_obj['no_of_comments'])

                # Convert the date string to a datetime object
                try:
                    date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
                except ValueError:
                    try:
                        date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
                    except Exception as e:
                        print(f"Error occurred: {e}")


                # Convert the datetime object to a timestamp string
                timestamp_string = date_object.strftime("%Y-%m-%d %H:%M:%S%z")


                # Print extracted values for debugging
                # print("title:", title)
                # print("category:", category)
                # print("content:", content)
                # print("no_of_photos:", no_of_photos)
                # print("date:", timestamp_string)
                # print("no_of_comments:", no_of_comments)

                # Define the query with named placeholders
                query = session.prepare(
                    """
                        INSERT INTO news_articles (url, title, category, content, no_of_photos, post_date, no_of_comments)
                        VALUES (:url, :title, :category, :content, :no_of_photos, :timestamp_string, :no_of_comments)
                    """
                )

                # Prepare a dictionary with named values
                named_values = {
                    "url": url,
                    "title": title,
                    "category": category,
                    "content": content,
                    "no_of_photos": no_of_photos,
                    "date": timestamp_string,
                    "no_of_comments": no_of_comments
                }

                # Execute the query with named values

                try:
                    session.execute(query, named_values)
                except Exception as e:
                    print(f"Error occurred: {e}")


# Close the Cassandra session and cluster connection
session.shutdown()
cluster.shutdown()
