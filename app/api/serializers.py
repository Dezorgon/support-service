from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Message, Ticket


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'author', 'date', 'text', 'ticket')


class CreateMessageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_tickets = Ticket.objects.filter(author=self.context["request"].user)
        self.fields["ticket"] = serializers.PrimaryKeyRelatedField(queryset=user_tickets)

    class Meta:
        model = Message
        fields = ('id', 'author', 'date', 'text', 'ticket')


class TicketSerializer(serializers.ModelSerializer):
    messages = serializers.HyperlinkedIdentityField(view_name='message-list', lookup_url_kwarg='ticket_pk')

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'status', 'author', 'messages')


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'title', 'status', 'author')


class NotPermittedCreateTicketSerializer(CreateTicketSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default=Ticket.Status.UNRESOLVED)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser', 'is_staff', 'date_joined', 'last_login')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'is_superuser', 'is_staff')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)

        return super().update(instance, validated_data)


class NotPermittedCreateUserSerializer(CreateUserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
