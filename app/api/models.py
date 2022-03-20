from django.contrib.auth.models import User
from django.db import models
from dry_rest_permissions.generics import (allow_staff_or_superuser,
                                           authenticated_users)


class Ticket(models.Model):
    class Status(models.TextChoices):
        RESOLVED = 'resolved'
        UNRESOLVED = 'unresolved'
        FROZEN = 'frozen'

    title = models.CharField(max_length=128)
    status = models.CharField(max_length=16, choices=Status.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return request.user == self.author

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return request.user == self.author

    class Meta:
        ordering = ('-id',)


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return request.user == self.ticket.author

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return request.user == self.ticket.author

    class Meta:
        ordering = ('-id',)
