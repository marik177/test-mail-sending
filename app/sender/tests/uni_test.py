from rest_framework import status
from rest_framework.test import APITestCase

from sender.models import Client


class TestStat(APITestCase):

    def test_client(self):
        client_count = Client.objects.all().count()
        client_create = {
            "phone_number": "79999999999",
            "tag": "crazy",
            "timezone": "UTC",
        }
        response = self.client.post("http://127.0.0.1:8000/api/v1/clients/", data=client_create)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Client.objects.all().count(), client_count + 1)
        # self.assertEqual(response.data["phone_number"], "79999999999")
        # self.assertIsInstance(response.data["phone_number"], str)
