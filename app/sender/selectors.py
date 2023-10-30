from .models import Client, MailSender, Message


def get_clients(mail_sender: MailSender):
    """"Filter all clients matching MailSender filters"""
    mail_sender_filters = mail_sender.filters.all()
    clients = Client.objects.all()
    for tag in mail_sender_filters:
        clients = clients.filter(tags=tag)
    return clients


def change_status_message_obj(id):
    """Set Message obj send_status as delivered """
    Message.objects.filter(id=id).update(send_status=True)
