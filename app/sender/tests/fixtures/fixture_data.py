from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
import pytz
import requests
from requests.exceptions import RequestException

utc = pytz.UTC


@pytest.fixture
def tag_1():
    from sender.models import Tag

    return Tag.objects.create(name="Movie")


@pytest.fixture
def tag_2():
    from sender.models import Tag

    return Tag.objects.create(name="222")


@pytest.fixture
def client_1(tag_1):
    from sender.models import Client, Tag

    client = Client.objects.create(
        phone_number="71111111111",
    )
    tag_phone_number, _ = Tag.objects.get_or_create(name=client.mobile_operator_code)

    client.tags.set([tag_1, tag_phone_number])
    return client


@pytest.fixture
def client_2(tag_1):
    from sender.models import Client, Tag

    client = Client.objects.create(
        phone_number="72222222222",
    )
    tag_phone_number, _ = Tag.objects.get_or_create(name=client.mobile_operator_code)

    client.tags.set([tag_1, tag_phone_number])
    return client


@pytest.fixture
def mail_sender_1(tag_1, tag_2):
    from sender.models import MailSender

    mail = MailSender.objects.create(
        sending_start=datetime.now(utc),
        sending_stop=datetime.now(utc) + timedelta(days=1),
        text="Test text",
    )
    mail.filters.set([tag_1, tag_2])

    return mail


# Create a custom pytest fixture for a Message instance
@pytest.fixture
def message_1(mail_sender_1, client_1):
    from sender.models import Message

    message = Message.objects.create(mail_sender=mail_sender_1, client=client_1)
    return message


# Mock the apply_async function in Celery tasks
@pytest.fixture(autouse=True)
def mock_celery_apply_async():
    with patch("sender.tasks.send_message.apply_async") as mock_apply_async:
        yield mock_apply_async


# Mock external API requests
@pytest.fixture
def mock_api_request():
    with patch.object(requests, "post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "OK"}
        yield mock_post


@pytest.fixture
def mock_api_request_failed():
    with patch.object(requests, "post") as mock_post:
        mock_post.return_value.status_code = 404
        mock_post.side_effect = RequestException
        yield mock_post
