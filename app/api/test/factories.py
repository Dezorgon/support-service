import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
