from celery import shared_task

from sender.external_service import send_message_task


@shared_task(bind=True, retry_backoff=True, retry_jitter=True)
def send_message(self, message, client, mail_sender):
    send_message_task(self, message, client, mail_sender)
