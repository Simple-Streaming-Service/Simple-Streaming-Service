from typing import Mapping

import requests

def make_query(query, variables, url, headers : Mapping[str, str | bytes | None] | None = None, timeout = 30):
    """
    Make query response
    """
    request = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, timeout=timeout)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))