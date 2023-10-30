from sender.services import get_clients


def test_return_clients(db, mail_sender_1, client_1, client_2, tag_1, tag_2):
    clients = get_clients(mail_sender_1)
    assert list(clients) == [client_2]


