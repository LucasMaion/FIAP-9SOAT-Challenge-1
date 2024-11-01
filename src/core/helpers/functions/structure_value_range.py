from typing import Optional, Tuple


def structure_value_range(
    min_value: Optional[float] = None, max_value: Optional[float] = None
) -> Tuple[Optional[float], Optional[float]]:
    if min_value or max_value:
        if not min_value:
            min_value = 0
        if not max_value:
            max_value = float("inf")
        if min_value > max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        return (min_value, max_value)
    return (None, None)
