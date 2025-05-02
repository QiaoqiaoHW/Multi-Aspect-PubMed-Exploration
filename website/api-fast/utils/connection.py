from opensearchpy import OpenSearch
from .config import username,password,host,port

client = OpenSearch(hosts = [{'host': host, 'port': port}],
                    http_auth =(username, password),
                    use_ssl = True,
                    verify_certs = False,
                    ssl_assert_hostname = False,
                    ssl_show_warn = False
                    )