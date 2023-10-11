from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import MailSender, Message
from .serializers import ClientSerializer, MailSenderSerializer, MessageSerializer
from .services import get_clients
from .tasks import send_message


@receiver(m2m_changed, sender=MailSender.filters.through, dispatch_uid="send_messages")
def send_messages(sender, instance: MailSender, action, **kwargs):
    if action != "post_add":
        return

    clients = get_clients(instance)
    if not clients:
        print("There are no clients matching the filter")
        return

    for client in clients:
        message = create_message(instance, client)
        send_message_async(instance, message, client)


def create_message(mail_sender, client):
    message = Message.objects.create(mail_sender=mail_sender, client=client)
    return MessageSerializer(message).data


def send_message_async(mail_sender, message, client):
    serializer_message = MessageSerializer(message).data
    serializer_client = ClientSerializer(client).data
    serializer_mail_sender = MailSenderSerializer(mail_sender).data

    task_args = (serializer_message, serializer_client, serializer_mail_sender)
    task_kwargs = (
        {"expires": mail_sender.sending_stop}
        if mail_sender.send_now()
        else {"eta": mail_sender.sending_start, "expires": mail_sender.sending_stop}
    )

    send_message.apply_async(task_args, **task_kwargs)


# @receiver(m2m_changed, sender=MailSender.filters.through, dispatch_uid="send_messages")
# def send_messages(sender, instance: MailSender, action, **kwargs):
#     clients = None
#     if action == "post_add":
#         clients = get_clients(instance)
#     if clients:
#         for client in clients:
#             message = Message.objects.create(mail_sender=instance, client=client)
#             serializer_message = MessageSerializer(message).data
#             serializer_client = ClientSerializer(client).data
#             serializer_mail_sender = MailSenderSerializer(instance).data
#             if instance.send_now():
#                 send_message.apply_async((serializer_message, serializer_client, serializer_mail_sender),
#                                          expires=instance.sending_stop)
#             else:
#                 send_message.apply_async((serializer_message, serializer_client, serializer_mail_sender),
#                                          eta=instance.sending_start,
#                                          expires=instance.sending_stop)
#     else:
#         print('There are no clients matching the filter')
