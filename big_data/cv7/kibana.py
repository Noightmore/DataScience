from elasticsearch import Elasticsearch


def main():
    from elasticsearch import Elasticsearch

    # create an Elasticsearch client
    es = Elasticsearch(['http://localhost:5601'], http_auth=('elastic', 'elastic'))

    # create the 'person' index
    es.indices.create(index='person')

    # create a new person document
    es.index(index='person', body={'firstname': 'John', 'lastname': 'Doe'})

    # search for the newly created person
    search_query = {'query': {'bool': {'must': [{'match': {'firstname': 'John'}}, {'match': {'lastname': 'Doe'}}]}}}
    result = es.search(index='person', body=search_query)

    # update the person document
    doc_id = result['hits']['hits'][0]['_id']
    es.update(index='person', id=doc_id, body={'doc': {'firstname': 'Jane', 'lastname': 'Doe'}})

    # print all person documents
    search_query = {'query': {'match_all': {}}}
    result = es.search(index='person', body=search_query)
    for hit in result['hits']['hits']:
        print(hit['_source'])

    # delete the person document
    es.delete(index='person', id=doc_id)

    # delete the person index
    es.indices.delete(index='person')


if __name__ == '__main__':
    main()
