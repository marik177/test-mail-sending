from rest_framework.response import Response

from sender.models import MailSender


class TestMailAPI:
    def test_mail_not_found(self, client, db):
        response = client.get("/api/v1/campaigns/")

        assert response.status_code != 404

    def test_mail_sender_get(self, client, db, mail_sender_1):
        response = client.get("/api/v1/campaigns/")
        assert response.status_code == 200

        test_data = response.json()

        assert isinstance(
            test_data, list
        ), "Check that a GET request to `/api/v1/campaings/` returns a list"

        assert len(test_data) == MailSender.objects.count()

        mail_sender = MailSender.objects.all()[0]
        test_mail_sender = test_data[0]

        assert "id" in test_mail_sender
        assert "sending_start" in test_mail_sender
        assert "sending_stop" in test_mail_sender
        assert "text" in test_mail_sender
        assert "filters" in test_mail_sender

        time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        assert test_mail_sender["id"] == mail_sender.id
        assert test_mail_sender["sending_start"] == mail_sender.sending_start.strftime(
            time_format
        )
        assert test_mail_sender["sending_stop"] == mail_sender.sending_stop.strftime(
            time_format
        )
        assert test_mail_sender["text"] == mail_sender.text
        assert test_mail_sender["filters"] == list(
            mail_sender.filters.values_list("name", flat=True)
        )

    def test_mail_sender_create(self, client, db, mail_sender_1, tag_1):
        mail_senders_count = MailSender.objects.count()

        data = {}
        response = client.post("/api/v1/campaigns/", data=data)
        assert (
            response.status_code == 400
        ), "Check that a POST request to `/api/v1/campaigns/` with incorrect data returns status 400"

        data = {
            "sending_start": "2023-10-07T18:44:06Z",
            "text": "Third",
            "sending_stop": "2023-10-10T14:44:13Z",
            "filters": [
                tag_1.name,
            ],
        }
        response = client.post(
            "/api/v1/campaigns/",
            data=data,
            format="json",
            content_type="application/json",
        )
        print(response.json())
        assert (
            response.status_code == 201
        ), "Check that a POST request to `/api/v1/campaigns/` with correct data returns status 201"

        test_data = response.json()

        assert isinstance(test_data, dict)
        assert test_data.get("sending_start") == data["sending_start"]
        assert test_data.get("sending_stop") == data["sending_stop"]
        assert test_data.get("text") == data["text"]
        assert test_data.get("sending_start") == data["sending_start"]

        assert mail_senders_count + 1 == MailSender.objects.count()

    def test_detail_report(self, client, db, mail_sender_1, message_1, monkeypatch):
        response = client.get(f"/api/v1/campaigns/{str(mail_sender_1.id)}/detail/")
        assert response.status_code == 200
        assert isinstance(response, Response)

    def test_full_report(self, client, db, mail_sender_1, message_1, monkeypatch):
        response = client.get("/api/v1/campaigns/full/")
        assert response.status_code == 200
        assert isinstance(response, Response)
