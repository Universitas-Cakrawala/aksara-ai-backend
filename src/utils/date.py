from datetime import date, datetime


def serialize_date(d):
    return d.isoformat() if isinstance(d, date) else None


TODAY = datetime.today().date()


MOTNTH_MAPPING = {
    "januari": 1,
    "februari": 2,
    "maret": 3,
    "april": 4,
    "mei": 5,
    "juni": 6,
    "juli": 7,
    "agustus": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "desember": 12,
}
