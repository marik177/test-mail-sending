from datetime import datetime

import pytz
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from requests.exceptions import RequestException
from rest_framework.response import Response

from .models import Message
from .services import to_datetime

logger = get_task_logger(__name__)


@shared_task(bind=True, retry_backoff=True, retry_jitter=True)
def send_message(self, message, client, mail_sender):
    mail_sender_start_time, mail_sender_stopt_time = to_datetime(
        mail_sender["sending_start"], mail_sender["sending_stop"]
    )

    if mail_sender_start_time <= datetime.now(pytz.UTC) <= mail_sender_stopt_time:
        try:
            header = {
                "Authorization": f"Bearer {settings.API_TOKEN}",
                "Content-Type": "application/json",
            }
            url = settings.URL + str(message["id"])
            data = {
                "id": message["id"],
                "phone": client["phone_number"],
                "text": mail_sender["text"],
            }
            r = requests.post(url=url, headers=header, json=data)
        except RequestException as e:
            logger.error(f"Message id: {message['id']} was not sent")
            raise self.retry(exc=e)
        else:
            if r.json()["message"] == "OK":
                logger.info(
                    f"The message with id: {data['id']} was delivered to client"
                )
                Message.objects.filter(id=data["id"]).update(send_status=True)
                return r.json()
    else:
        return Response("Mail sending time comes to the end")
