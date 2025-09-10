from decouple import config
import itertools
import requests


def safe_float(value, default=0.0):
    return float(value) if value is not None else default


def safe_convert_to_int(value):
    try:
        # Convert to float first to handle float and int smoothly, then to int
        return int(float(value))
    except (ValueError, TypeError):
        return 0


def clean_and_upper(value):
    if value is None or value == "":
        return ""
    # Ensure the value is treated as a string regardless of its original type
    value = str(value)
    return value.strip().upper()
