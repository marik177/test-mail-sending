from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from .models import Client, MailSender, Message, Tag
from .serializers import (
    ClientSerializer,
    ClientWriteSerializer,
    MailSenderReportSerializer,
    MailSenderSerializer,
    MessageSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ClientViewSet(viewsets.ModelViewSet):
    # serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ClientSerializer
        else:
            return ClientWriteSerializer


class MailSenderViewSet(viewsets.ModelViewSet):
    serializer_class = MailSenderSerializer
    queryset = MailSender.objects.all()

    @action(
        detail=True,
        methods=[
            "GET",
        ],
        url_path="detail",
        url_name="detail",
    )
    def detail_report(self, request, pk=None):
        mail_sender = get_object_or_404(MailSender, id=pk)
        messages = mail_sender.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=[
            "GET",
        ],
        url_path="full",
        url_name="full",
    )
    def full_report(self, request):
        all_mail_sendings = MailSender.objects.all()
        serializer = MailSenderReportSerializer(all_mail_sendings, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
