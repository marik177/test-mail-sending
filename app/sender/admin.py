from django.contrib import admin

from .models import Client, MailSender, Message, Tag


class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "timezone")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "send_status", "mail_sender", "client")


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class MailSenderAdmin(admin.ModelAdmin):
    list_display = ("id", "sending_start", "text", "sending_stop")


admin.site.register(Message, MessageAdmin)
admin.site.register(MailSender, MailSenderAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Tag, TagAdmin)
