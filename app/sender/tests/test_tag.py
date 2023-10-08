import pytest
from sender.models import Tag


class TestTagAPI:

    @pytest.mark.django_db(transaction=True)
    def test_tags_not_found(self, client):
        response = client.get('/api/v1/tags/')

        assert response.status_code != 404

    @pytest.mark.django_db(transaction=True)
    def test_tag_get(self, client, tag_1, tag_2):
        response = client.get('/api/v1/tags/')
        assert response.status_code == 200

        test_data = response.json()

        assert type(test_data) == list, 'Check that a GET request to `/api/v1/tags/` returns a list'

        assert len(test_data) == Tag.objects.count()

        tag = Tag.objects.all()[0]
        test_tag = test_data[0]

        assert 'name' in test_tag

        assert test_tag['name'] == tag.name

    def test_tag_create(self, db, client, tag_1, tag_2):
        tag_count = Tag.objects.count()

        data = {}
        response = client.post('/api/v1/tags/', data=data)
        assert response.status_code == 400, \
            'Check that a POST request to `/api/v1/tags/` with incorrect data returns status 400'

        data = {'name': 'Football'}
        response = client.post('/api/v1/tags/', data=data)
        print(response.json())
        assert response.status_code == 201, \
            'Check that a POST request to `/api/v1/tags/` with correct data returns status 201'

        test_data = response.json()

        msg_error = 'Check that a POST request to `/api/v1/tags/` returns a dictionary with the new tag data'
        assert type(test_data) == dict, msg_error
        assert test_data.get('name') == data['name'], msg_error

        assert tag_count + 1 == Tag.objects.count(), \
            'Check that a POST request to `/api/v1/tags/` creates a tag'
