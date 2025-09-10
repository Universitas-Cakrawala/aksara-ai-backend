from src.constants import (
    MONTHS,
)
import re
import os
from datetime import datetime
import pytz


def format_size(size):
    # Example implementation; adjust as needed
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def is_safe_filename(filename):
    return os.path.basename(filename) == filename


def validate_file_size(file_content, max_size=100 * 1024 * 1024):
    return len(file_content) <= max_size


def allowed_file_type_general(filename):
    allowed_extensions = {
        "txt",
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "mp3",
        "wav",
        "mp4",
        "mkv",
        "avi",
        "mov",
        "webp",
    }
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def allowed_file_type_document(filename):
    allowed_extensions = {
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
    }
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def allowed_file_type_barbuk(filename):
    allowed_extensions = {
        "png",
        "jpg",
        "jpeg",
        "webp",
        "pdf",
    }
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def allowed_file_type_foto(filename):
    allowed_extensions = {
        "png",
        "jpg",
        "jpeg",
        "webp",
    }
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def allowed_file_insert_data(filename):
    allowed_extensions = {
        "xlsx",
        "xls",
        "csv",
    }
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def format_date(date_str):
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    local_dt = dt.astimezone(jakarta_tz)
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")


# Make a regular expression
# for validating an Email
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


# Define a function for
# for validating an Email
def validateEmail(email):

    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def validate_months(month):
    if month in MONTHS:
        return True
    else:
        return False
