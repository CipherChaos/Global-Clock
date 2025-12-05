import math
import pytz
from datetime import datetime


def deg_to_rad(degrees):
    """Convert degrees to radians."""
    return degrees * (math.pi / 180)


def get_next_style(current_style, style_dict):
    """Get the next style from a dictionary, avoiding duplicates."""
    keys = list(style_dict.keys())
    current_index = keys.index(
        next(
            key for key, value in style_dict.items() if value == current_style)
    )

    for i in range(1, len(keys) + 1):
        next_index = (current_index + i) % len(keys)
        if style_dict[keys[next_index]] != current_style:
            return style_dict[keys[next_index]]
    return current_style


def get_local_time(tz_name):
    """Get current time in a specific timezone."""
    tz = pytz.timezone(tz_name)
    return datetime.now().astimezone(tz)
