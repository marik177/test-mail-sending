from datetime import datetime

import pytz

from .models import Client, MailSender


def get_clients(mail_sender: MailSender):
    mail_sender_filters_ids = mail_sender.filters.values_list("id", flat=True)
    clients = Client.objects.all()
    return [
        client
        for client in clients
        if sorted(client.tags.values_list("id", flat=True)) == sorted(mail_sender_filters_ids)
    ]


def to_datetime(start, stop):
    time_formats = ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%fZ"]

    for time_format in time_formats:
        try:
            start = datetime.strptime(start, time_format).astimezone(pytz.utc)
            stop = datetime.strptime(stop, time_format).astimezone(pytz.UTC)
            return start, stop
        except ValueError:
            continue
    raise ValueError("Time format does not supported")
