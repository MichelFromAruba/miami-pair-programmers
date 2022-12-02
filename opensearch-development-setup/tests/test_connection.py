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








