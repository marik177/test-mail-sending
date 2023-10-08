from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import MailSender, Message
from .services import get_clients
from .tasks import send_message
from .serializers import MessageSerializer, ClientSerializer, MailSenderSerializer


@receiver(m2m_changed, sender=MailSender.filters.through, dispatch_uid="send_messages")
def send_messages(sender, instance: MailSender, action, **kwargs):
    clients = None
    if action == "post_add":
        clients = get_clients(instance)
    if clients:
        for client in clients:
            message = Message.objects.create(mail_sender=instance, client=client)
            serializer_message = MessageSerializer(message).data
            serializer_client = ClientSerializer(client).data
            serializer_mail_sender = MailSenderSerializer(instance).data
            if instance.send_now():
                send_message.apply_async((serializer_message, serializer_client, serializer_mail_sender),
                                         expires=instance.sending_stop)
            else:
                send_message.apply_async((serializer_message, serializer_client, serializer_mail_sender),
                                         eta=instance.sending_start,
                                         expires=instance.sending_stop)
    else:
        print('There are no clients matching the filter')
