from re import compile, RegexFlag
from typing import Callable

query_pattern = compile(
    r":(?P<type>\w+) (?P<query>.*?) ?(?=:)",
    RegexFlag.S | RegexFlag.IGNORECASE
)

def search(data, query : str, query_processor) -> list:
    parsed = ":any " + query + ":"
    parsed = query_pattern.finditer(parsed)
    query_dict = {
        match.group("type"): match.group("query") for match in parsed
    }

    return data