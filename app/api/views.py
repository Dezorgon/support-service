from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import filters, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.mixins import GetSerializerMixin
from api.models import Message, Ticket
from api.permissions import IsStaffOrMe
from api.serializers import (CreateMessageSerializer, CreateTicketSerializer,
                             CreateUserSerializer, MessageSerializer,
                             NotPermittedCreateTicketSerializer,
                             NotPermittedCreateUserSerializer,
                             TicketSerializer, UserSerializer)
from api.tasks import send_email_to_all_users


class GetMessageViewSet(GetSerializerMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):

    queryset = Message.objects.all()
    permission_classes = (DRYPermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['date', 'text']

    serializer_classes = {
        'default': MessageSerializer,
    }

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_pk')
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        if self.action == 'list':
            return self.queryset.filter(ticket=ticket)

        return self.queryset


class MessageViewSet(GetSerializerMixin, ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = (DRYPermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['date', 'text']

    serializer_classes = {
        'create': CreateMessageSerializer,
        'update': CreateMessageSerializer,
        'default': MessageSerializer,
    }

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(author=self.request.user)
        return self.queryset


class TicketViewSet(GetSerializerMixin, ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = (DRYPermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'status']

    serializer_classes = {
        'create': {'user': NotPermittedCreateTicketSerializer,
                   'staff': CreateTicketSerializer},
        'update': {'user': NotPermittedCreateTicketSerializer,
                   'staff': CreateTicketSerializer},
        'default': TicketSerializer,
    }

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_staff:
                return self.queryset
            return self.queryset.filter(author=self.request.user)
        return self.queryset


class UserViewSet(GetSerializerMixin, ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsStaffOrMe,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'status']

    serializer_classes = {
        'create': {'user': NotPermittedCreateUserSerializer,
                   'staff': CreateUserSerializer},
        'update': {'user': NotPermittedCreateUserSerializer,
                   'staff': CreateUserSerializer},
        'default': UserSerializer,
    }

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_staff:
                return self.queryset
            return self.queryset.filter(pk=self.request.user.pk)
        return self.queryset


@api_view(['POST'])
def spam_email(request):
    text = request.data['email_text']
    send_email_to_all_users.delay(text)
    return Response({"message": "ok"})
