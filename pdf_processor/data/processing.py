from typing import Any, Dict, List


def rowify(main_data: Dict[str, Any], extra: Any) -> List[Any]:
    f"""
    Convert dict of pdf data to rows for relational db.
    """
    data = []

    for k in main_data:
        data.append(extra + [k] + [main_data[k][k2] for k2 in main_data[k]])
    return data
