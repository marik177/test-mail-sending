from .models import Client, MailSender
from datetime import datetime


def get_clients(mail_sender: MailSender):
    mail_sender_filters_ids = mail_sender.filters.values_list('id', flat=True)
    clients = Client.objects.all()
    return [client for client in clients
            if sorted(client.tags.values_list('id', flat=True)) == sorted(mail_sender_filters_ids)]


def to_datetime(start, stop):
    time_format = "%Y-%m-%dT%H:%M:%S%z"
    start = datetime.strptime(start, time_format)
    stop = datetime.strptime(stop, time_format)
    return start, stop
