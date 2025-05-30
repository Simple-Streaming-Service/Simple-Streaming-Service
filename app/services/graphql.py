from typing import Mapping

import requests
from requests import Response


def make_query(query, variables, url, headers : Mapping[str, str | bytes | None] | None = None):
    """
    Make query response
    """
    request = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed to run by returning code of {request.status_code}.\nContent: {request.content}\nQuery: {query}\nVariables: {variables}")