from opensearchpy import OpenSearch


def create_client():
    host = 'localhost'
    port = 9200
    auth = ('admin', 'admin')  # For testing only. Don't store credentials in code.

    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    return client


def create_index(index_name):

    index_body = {
        'settings': {
            'index': {
                'number_of_shards': 4
            }
        }
    }
    client = create_client()
    response = client.indices.create(index_name, body=index_body)
    print('\nCreating index:')
    print(response)

    return response


def delete_index(index_name):
    # Delete the index.
    client = create_client()

    response = client.indices.delete(
        index=index_name
    )

    print('\nDeleting index:')
    print(response)


def add_document(index_name, id, document):

    client = create_client()
    # Add a document to the index.

    response = client.index(
        index=index_name,
        body=document,
        id=id,
        refresh=True
    )
    print('\nAdding document:')
    print(response)

    return response

def test_create_connection():
    client = create_client()

    assert client is not None


def test_create_index():
    index_name = 'python-test-index'

    try:
        response = create_index(index_name)
    except:
        delete_index(index_name)
        print('deleting index already there')

    response = create_index(index_name)

    assert response is not None


def test_add_document():
    index_name = 'python-test-index'
    document = {
        'title': 'Moneyball',
        'director': 'Bennett Miller',
        'year': '2011'
    }
    id = '1'
    response = add_document(index_name, id, document)

    assert response is not None


def test_search_document():
    client = create_client()
    index_name = 'python-test-index'

    # Search for the document.
    q = 'Moneyball'
    query = {
        'size': 5,
        'query': {
            'multi_match': {
                'query': q,
                'fields': ['title']
            }
        }
    }

    response = client.search(
        body=query,
        index=index_name
    )
    print('\nSearch results:')
    print(response)







