import json

import pytest
from rest_framework.test import APIClient

from sender.models import Client

factory = APIClient()


class TestClientAPI:

    @pytest.mark.django_db(transaction=True)
    def test_client_not_found(self, client):
        response = client.get('/api/v1/clients/')

        assert response.status_code != 404

    @pytest.mark.django_db(transaction=True)
    def test_clients_get(self, client, client_1, client_2):
        response = client.get('/api/v1/clients/')
        assert response.status_code == 200

        test_data = response.json()

        assert isinstance(test_data, list), 'Check that a GET request to `/api/v1/clients/` returns a list'

        assert len(test_data) == Client.objects.count()

        client1 = Client.objects.all()[0]
        test_client1 = test_data[0]

        assert 'id' in test_client1
        assert 'phone_number' in test_client1
        assert 'tags' in test_client1
        assert 'timezone' in test_client1

        assert test_client1['id'] == client1.id
        assert test_client1['phone_number'] == client1.phone_number
        assert test_client1['tags'] == list(client1.tags.values_list('name', flat=True))
        assert test_client1['timezone'] == client1.timezone

    def test_client_create(self, client, db, client_1, client_2, tag_1):
        clients_count = Client.objects.count()

        data = {}
        response = client.post('/api/v1/clients/', data=data)
        assert response.status_code == 400, \
            'Check that a POST request to `/api/v1/clients/` with incorrect data returns status 400'

        data = {
            'phone_number': '72222222223',
            'tags': [tag_1.name],
        }
        response = client.post('/api/v1/clients/', data=data, format='json', content_type="application/json")
        assert response.status_code == 201, \
            'Check that a POST request to `/api/v1/clients/` with correct data returns status 201'

        test_data = response.json()
        msg_error = 'Check that a POST request to `/api/v1/clients/` ' \
                    'returns a dictionary with the new client data'
        assert isinstance(test_data, dict), msg_error
        assert test_data.get('phone_number') == data['phone_number'], msg_error

        data['tags'].append(data['phone_number'][1:4])  # add mobile_operator_code to tags

        assert sorted(test_data.get('tags')) == sorted(data['tags']), msg_error

        assert clients_count + 1 == Client.objects.count(), \
            'Check that a POST request to `/api/v1/tags/` creates a client'

    def test_client_does_not_create_with_not_7_code(self, client, db, client_1, client_2, tag_1):
        data = {
            'phone_number': '12222222222',
            'tags': [tag_1.name],
        }
        response = client.post('/api/v1/clients/', data=data, format='json', content_type="application/json")
        assert response.status_code == 400

    def test_client_does_not_create_with_not_right_format_phone_number(self, client, db, client_1, client_2, tag_1):
        data = {
            'phone_number': '722W2222222',
            'tags': [tag_1.name],
        }
        response = client.post('/api/v1/clients/', data=data, format='json', content_type="application/json")
        assert response.status_code == 400
        assert response.json()['phone_number'] == \
               ['The phone number must be in format 7XXXXXXXXXX (X - number from 0 to 9) and has the length of 11']

    def test_client_delete(self, client, db, client_1, client_2, tag_1):
        clients_count = Client.objects.count()

        response = client.delete('/api/v1/clients/' + str(client_1.id) + '/')
        assert response.status_code == 204
        assert clients_count - 1 == Client.objects.count()
