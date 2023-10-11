from datetime import datetime, timedelta

import pytest
import pytz

utc = pytz.UTC


@pytest.fixture
def tag_1():
    from sender.models import Tag
    return Tag.objects.create(name='Movie')


@pytest.fixture
def tag_2():
    from sender.models import Tag
    return Tag.objects.create(name='Hockey')


@pytest.fixture
def client_1(tag_1):
    from sender.models import Client
    client = Client.objects.create(
        phone_number="71111111111",
    )

    client.tags.set([tag_1])
    return client


@pytest.fixture
def client_2(tag_2):
    from sender.models import Client
    client = Client.objects.create(
        phone_number="72222222222",
    )
    client.tags.set([tag_2])
    return client


@pytest.fixture
def mail_sender_1(tag_1, tag_2):
    from sender.models import MailSender
    mail = MailSender.objects.create(
        sending_start=datetime.now(utc),
        sending_stop=datetime.now(utc) + timedelta(days=1),
        text='Test text',
    )

    mail.filters.set([tag_1, tag_2])

    return mail
