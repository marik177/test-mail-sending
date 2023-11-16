from datetime import timedelta
from unittest.mock import patch

import pytest
import pytz
from requests.exceptions import RequestException
from sender.external_service import request_to_external_service, send_message_task
from sender.models import MailSender
from sender.serializers import ClientSerializer, MailSenderSerializer, MessageSerializer
from sender.signals import send_messages  # Import your actual signal handler
from sender.tasks import send_message  # Import your actual Celery task

utc = pytz.UTC


class TestMessageSendingAPI:
    # Test the send_messages signal handler
    # @pytest.mark.django_db
    # def test_send_messages_signal(self, client_1, mail_sender_1):
    #     with patch("sender.signals.get_clients") as mock_get_clients:
    #         mock_get_clients.return_value = [client_1]
    #         send_messages(
    #             sender=MailSender.filters.through,
    #             instance=mail_sender_1,
    #             action="post_add",
    #         )
    #
    #         mock_get_clients.assert_called()

    # Test the send_message Celery task
    # @pytest.mark.django_db
    # def test_send_message_task_ok(
    #     self, mail_sender_1, client_1, message_1, mock_api_request
    # ):
    #     serializer_message = MessageSerializer(message_1).data
    #     serializer_client = ClientSerializer(client_1).data
    #     serializer_mail_sender = MailSenderSerializer(mail_sender_1).data
    #
    #     # Call the send_message task
    #     result = send_message(
    #         serializer_message, serializer_client, serializer_mail_sender
    #     )
    #
    #     # Assert that the API request was made
    #     assert result == {"message": "OK"}

    @pytest.mark.django_db
    def test_send_message_task_failed(
        self, mail_sender_1, client_1, message_1, mock_api_request_failed
    ):
        serializer_message = MessageSerializer(message_1).data
        serializer_client = ClientSerializer(client_1).data
        serializer_mail_sender = MailSenderSerializer(mail_sender_1).data

        with pytest.raises(RequestException):
            # Call the send_message task
            send_message(serializer_message, serializer_client, serializer_mail_sender)

    # @pytest.mark.django_db
    # def test_send_message_time_come_to_the_end(
    #     self, mail_sender_1, client_1, message_1, mock_api_request
    # ):
    #     mail_sender_1.sending_stop = mail_sender_1.sending_stop - timedelta(days=2)
    #     serializer_message = MessageSerializer(message_1).data
    #     serializer_client = ClientSerializer(client_1).data
    #     serializer_mail_sender = MailSenderSerializer(mail_sender_1).data
    #
    #     response = send_message(
    #         serializer_message, serializer_client, serializer_mail_sender
    #     )
    #
    #     assert response.data == "Mail sending time comes to the end"
