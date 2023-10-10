from datetime import datetime, timedelta

import pytest
from unittest.mock import Mock, patch
from django.test import TestCase
from django.db.models.signals import m2m_changed
from sender.models import MailSender, Client, Message
from sender.signals import send_messages  # Import your actual signal handler
from sender.tasks import send_message  # Import your actual Celery task
from sender.services import get_clients, to_datetime  # Import your utility functions
from sender.serializers import MessageSerializer, ClientSerializer, MailSenderSerializer
from django.conf import settings
import pytz
import requests

utc = pytz.UTC


# Create a custom pytest fixture for a MailSender instance with filters
@pytest.fixture
def mail_sender_instance():
    return MailSender.objects.create(
        sending_start=datetime.now(utc),
        sending_stop=datetime.now(utc) + timedelta(days=1),
        text='Test text',
    )


# Create a custom pytest fixture for a Client instance with tags
@pytest.fixture
def client_instance(mail_sender_instance):
    client = Client.objects.create(
        phone_number="72222222222",
    )
    client.tags.add(mail_sender_instance.filters.first())
    return client


# Create a custom pytest fixture for a Message instance
@pytest.fixture
def message_instance(mail_sender_instance, client_instance):
    message = Message.objects.create(mail_sender=mail_sender_instance, client=client_instance)
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


# Test the send_messages signal handler
@pytest.mark.django_db
def test_send_messages_signal(
        mail_sender_instance, client_instance, message_instance, mock_celery_apply_async, mock_api_request
):
    # Connect the signal
    m2m_changed.connect(send_messages, sender=MailSender.filters.through)

    # Add a client to the MailSender filters
    mail_sender_instance.filters.add(client_instance.tags.first())

    # Disconnect the signal
    m2m_changed.disconnect(send_messages, sender=MailSender.filters.through)

    # Assert that the apply_async function was called
    assert mock_celery_apply_async.called


# Test the send_message Celery task
@pytest.mark.django_db
def test_send_message_task(mail_sender_instance, client_instance, message_instance, mock_api_request):
    # Configure the necessary data
    serializer_message = MessageSerializer(message_instance).data
    serializer_client = ClientSerializer(client_instance).data
    serializer_mail_sender = MailSenderSerializer(mail_sender_instance).data

    # Set the current time within the sending window
    # current_time = mail_sender_instance.sending_start
    # with patch("django.utils.timezone.now") as mock_now:
    #     mock_now.return_value = current_time

    # Call the send_message task
    result = send_message(serializer_message, serializer_client, serializer_mail_sender)

    # Assert that the API request was made
    assert result == {"message": "OK"}
