from rest_framework import serializers
from .models import Client, Tag, MailSender, Message


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ClientSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(),
                                        slug_field='name', many=True)

    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'tags', 'timezone')


class ClientWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'tags', 'timezone')

    def create(self, validated_data):
        tags_names = validated_data.pop("tags", None)
        client = Client.objects.create(**validated_data)
        mobile_operator_code = validated_data['phone_number'][1:4]
        tag_mobile_operator_code, created = Tag.objects.get_or_create(name=mobile_operator_code)
        tags = [tag_mobile_operator_code]
        if tags_names:
            for tag_name in tags_names:
                t, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(t)
        client.tags.set(tags)
        return client


class MailSenderSerializer(serializers.ModelSerializer):
    filters = serializers.SlugRelatedField(queryset=Tag.objects.all(),
                                           slug_field='name', many=True)

    class Meta:
        model = MailSender
        fields = ('id', 'sending_start', 'text', 'sending_stop', 'filters')

    def create(self, validated_data):
        filters = validated_data.pop('filters')
        mail_sender = MailSender.objects.create(**validated_data)
        mail_sender.filters.set(filters)
        return mail_sender


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MailSenderReportSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = MailSender
        fields = ('id', 'text', 'messages')
