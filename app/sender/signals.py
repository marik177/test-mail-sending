from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import MailSender
from .services import send_to_all_clients


@receiver(m2m_changed, sender=MailSender.filters.through, dispatch_uid="send_messages")
def send_messages(sender, instance: MailSender, action, **kwargs):
    if action != "post_add":
        return
    send_to_all_clients(instance)

