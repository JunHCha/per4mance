import datetime
from typing import Any, Dict, List

from per4mance import db_engine


def fetch_all(query: Any) -> List[Dict[str, Any]]:
    data = db_engine.connect().execute(query).all()
    columns = [str(col.name) for col in query.columns]
    listed = [list(each) for each in data]
    values = list()
    for value in listed:
        curr = []
        for each in value:
            curr.append(
                each
                if type(each) != datetime.datetime
                else each.strftime("%Y-%m-%d %H:%M:%S")
            )
        values.append(tuple(curr))
    data = [dict(zip(columns, value)) for value in values]
    return data
