import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

TIME_ZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Tag(models.Model):
    name = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class MailSender(models.Model):
    sending_start = models.DateTimeField(verbose_name="Sending start time")
    text = models.TextField(max_length=255, verbose_name="Message text")
    sending_stop = models.DateTimeField(verbose_name="Sending stop time")
    filters = models.ManyToManyField(
        Tag, verbose_name="Filter", blank=True, related_name="mail_sender"
    )

    class Meta:
        verbose_name = "MailSender"
        verbose_name_plural = "MailSenders"

    def send_now(self) -> bool:
        return self.sending_start <= timezone.now() <= self.sending_stop


class Client(models.Model):
    validate_phone = RegexValidator(
        regex=r"^7\d{10}$",
        message="The phone number must be in format "
                "7XXXXXXXXXX (X - number from 0 to 9) and has the length of 11",
    )
    phone_number = models.CharField(
        verbose_name="Phone number",
        validators=[validate_phone],
        unique=True,
        max_length=11,
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="clients")
    timezone = models.CharField(
        verbose_name="Client time zone",
        max_length=32,
        choices=TIME_ZONES,
        default="UTC",
    )

    @property
    def mobile_operator_code(self) -> str:
        return self.phone_number[1:4]

    def __str__(self):
        return f"Client {self.id} has a phone number {self.phone_number}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    send_status = models.BooleanField(default=False)
    mail_sender = models.ForeignKey(
        MailSender, on_delete=models.CASCADE, related_name="messages"
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="messages"
    )

    def __str__(self):
        return f"Message {self.id} in the mail sending {self.mail_sender} for client {self.client}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

