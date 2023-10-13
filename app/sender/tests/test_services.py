from datetime import datetime

import pytz

from sender.services import get_clients, to_datetime


def test_return_clients(db, mail_sender_1, client_1, client_2, tag_1, tag_2):
    clients = get_clients(mail_sender_1)
    assert isinstance(clients, list)
    assert clients == [client_2]


def test_to_datetime():
    start = "2023-10-12T14:42:20.902798Z"
    stop = "2024-10-15T19:42:20.000798Z"
    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    result = to_datetime(start, stop)
    dt_start = datetime.strptime(start, time_format).astimezone(pytz.utc)
    dt_stop = datetime.strptime(stop, time_format).astimezone(pytz.utc)
    assert dt_start, dt_stop == result
