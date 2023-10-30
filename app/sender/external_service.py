import requests
from celery.utils.log import get_task_logger
from django.conf import settings
from requests.exceptions import RequestException
from rest_framework import status

from sender.selectors import change_status_message_obj

logger = get_task_logger(__name__)


def send_message_task(task, message, client, mail_sender):
    """Send a request to an external API and recieve an answer"""
    response, message_id = request_to_external_service(task, message, client, mail_sender)
    if response.json()["message"] == "OK":
        logger.info(
            f"The message with id: {message_id} was delivered to client"
        )
        change_status_message_obj(message_id)
        return response.json()
    return response.status_code


def request_to_external_service(task, message, client, mail_sender):
    """Make request to external service"""
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
        raise task.retry(exc=e)
    return r, data["id"]

