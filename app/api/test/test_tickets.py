import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.test.api import post_ticket
from api.test.fixtures import auth_user, get_auth_user


@pytest.mark.django_db
def test_unauthorized_post_ticket(django_db_setup):
    post_ticket('some title', APIClient(), 401)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, status_code', [
        pytest.param(
            '',
            400
        ),
        pytest.param(
            'some title',
            201
        ),
    ]
)
def test_post_ticket(data, status_code, django_db_setup, auth_user):
    post_ticket(data, auth_user, status_code)


@pytest.mark.django_db
def test_unauthorized_get_tickets(django_db_setup):
    url = reverse('ticket-list')
    response = APIClient().get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_tickets(django_db_setup, auth_user):
    post_ticket('some title', auth_user, 201)

    url = reverse('ticket-list')
    response = auth_user.get(url)
    result = response.json()['results']

    for ticket in result:
        assert ticket['author'] == auth_user.user.id

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_non_exist_ticket(django_db_setup, auth_user):
    url = reverse('ticket-detail', args=[1337])
    response = auth_user.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_foreign_ticket(django_db_setup, auth_user):
    ticket = post_ticket('some title', get_auth_user(), 201)

    url = reverse('ticket-detail', args=[ticket['id']])
    response = auth_user.get(url)
    assert response.status_code == 403
