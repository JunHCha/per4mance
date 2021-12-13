import datetime
from typing import Any, Dict, List

from per4mance import db_engine


async def fetch_one(query: Any) -> Dict[str, Any]:
    async with db_engine.connect() as conn:
        res = await conn.execute(query)
    data = res.fetchone()
    if data is None:
        return None
    columns = [str(col.name) for col in query.columns]
    values = [value for value in list(data)]
    data = dict(zip(columns, values))
    return data


async def fetch_all(query: Any) -> List[Dict[str, Any]]:
    async with db_engine.connect() as conn:
        res = await conn.execute(query)
    data = res.fetchall()
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
