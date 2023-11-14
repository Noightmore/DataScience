import json
import os
from elasticsearch import Elasticsearch
import urllib3

'''
    to install:
    docker run --name es-idnes --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.11.1

'''


def connect():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "https"}],
                       basic_auth=('elastic', 'tDBf9G2VL=U-KmpELxYy'), verify_certs=False)

    return es


def create_mapping(es, index_name):
    index_settings = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "category": {"type": "keyword"},
                "content": {"type": "text"},
                "no_of_photos": {"type": "integer"},
                "date": {"type": "date"},
                "no_of_comments": {"type": "integer"},
                "url": {"type": "text"}
            }
        }
    }

    # Check if the index exists
    if not es.indices.exists(index=index_name):
        # Try to create the index
        try:
            es.indices.create(index=index_name, body=index_settings, ignore=400)
            print(f"Index '{index_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create index '{index_name}': {e}")
    else:
        print(f"Index '{index_name}' already exists.")


def print_index_mappings(es, index_name):
    mappings = es.indices.get_mapping(index=index_name)
    print(f"Mappings for index '{index_name}':")
    print(mappings)


def load_data_from_jsons(es, index):
    json_folder = '/home/rob/Programming/DataScience/big_data2/data'

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
                        #print(date)
                        dato = date

                        # Prepare a dictionary with named values
                        document = {
                            "title": title,
                            "category": category,
                            "content": content,
                            "no_of_photos": no_of_photos,
                            "date": dato,
                            "no_of_comments": no_of_comments,
                            "url": url
                        }

                        # elastic query:
                        try:
                            add_record(es, index, document)
                        except Exception as e:
                            print(f"Error occurred: {e}")
                    except Exception as e:
                        print(f"Error occurred: {e}")
    print("data loaded")


def add_record(es, index_name, document):
    es.index(index=index_name, body=document)


def delete_all_mappings(es, index_name):
    empty_mapping = {}  # An empty mapping

    es.indices.put_mapping(index=index_name, body=empty_mapping)


def delete_index(es, index_name):
    es.indices.delete(index=index_name)


def main():
    index = 'idnes'
    my_elastic = connect()
    delete_all_mappings(my_elastic, index)
    delete_index(my_elastic, index)
    create_mapping(my_elastic, index)
    print_index_mappings(my_elastic, index)
    load_data_from_jsons(my_elastic, index)


if __name__ == '__main__':
    main()
