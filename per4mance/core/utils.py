from typing import Any, Dict, List

from per4mance import db_engine


def fetch_all(query: Any) -> List[Dict[str, Any]]:
    data = db_engine.connect().execute(query).all()
    columns = [str(col.name) for col in query.columns]
    data = [dict(zip(columns, each)) for each in data]
    return data
