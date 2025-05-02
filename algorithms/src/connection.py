from opensearchpy import OpenSearch

from .config import client, local_client

def connect_opensearch(host,port,username,password,verify_certs=True):
    client = OpenSearch(hosts = [{'host': host, 'port': port}],
                        http_auth =(username, password),
                        use_ssl = True,
                        verify_certs = verify_certs,
                        ssl_assert_hostname = False,
                        ssl_show_warn = False,
                        timeout=30
                        )
    return client


client = connect_opensearch(
    client["host"],
    client["port"],
    client["username"],
    client["password"],
)

local_client = connect_opensearch(
    local_client["host"],
    local_client["port"],
    local_client["username"],
    local_client["password"],
    verify_certs=False,
)