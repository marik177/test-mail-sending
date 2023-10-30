from .models import Client, MailSender, Message
from .selectors import get_clients
from .serializers import (ClientSerializer, MailSenderSerializer,
                          MessageSerializer)
from .tasks import send_message


def start_or_postpone_mail_sender(mail_sender: MailSender):
    """Scheduler for MailSender"""
    send_or_wait = (
        {"expires": mail_sender.sending_stop}
        if mail_sender.send_now()
        else {"eta": mail_sender.sending_start, "expires": mail_sender.sending_stop}
    )
    return send_or_wait


def send_message_to_client(mail_sender, message, client):
    """Send message to a single client"""
    serialized_data = _prepare_data(mail_sender, message, client)
    send_or_wait = start_or_postpone_mail_sender(mail_sender)
    send_message.apply_async(serialized_data, **send_or_wait)


def send_to_all_clients(mailsender: MailSender):
    """Send messages to all clients with matching tags"""
    clients = get_clients(mailsender)
    for client in clients:
        message = create_message_obj(mailsender, client)
        send_message_to_client(mailsender, message, client)


def create_message_obj(mail_sender, client):
    """create Message object"""
    message = Message.objects.create(mail_sender=mail_sender, client=client)
    return message


def _prepare_data(mail_sender, message, client):
    serializer_message = MessageSerializer(message).data
    serializer_client = ClientSerializer(client).data
    serializer_mail_sender = MailSenderSerializer(mail_sender).data
    return serializer_message, serializer_client, serializer_mail_sender

