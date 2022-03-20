import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.test.api import post_message, post_ticket
from api.test.fixtures import auth_user, get_auth_user


@pytest.mark.django_db
def test_unauthorized_post_message(django_db_setup):
    post_message('some text', 1, APIClient(), 401)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'text, status_code', [
        pytest.param(
            '',
            400
        ),
        pytest.param(
            'some text',
            201
        ),
    ]
)
def test_post_message(text, status_code, django_db_setup, auth_user):
    ticket = post_ticket('some title', auth_user, 201)
    post_message(text, ticket['id'], auth_user, status_code)


@pytest.mark.django_db
def test_post_message_to_foreign_ticket(django_db_setup, auth_user):
    ticket = post_ticket('some title', get_auth_user(), 201)
    post_message('some text', ticket['id'], auth_user, 400)


@pytest.mark.django_db
def test_post_message_to_non_exist_ticket(django_db_setup, auth_user):
    post_message('some text', 1337, auth_user, 400)


@pytest.mark.django_db
def test_unauthorized_get_messages(django_db_setup):
    url = reverse('message-list')
    response = APIClient().get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_messages(django_db_setup, auth_user):
    ticket = post_ticket('some title', auth_user, 201)
    post_message('some text', ticket['id'], auth_user, 201)

    url = reverse('message-list')
    response = auth_user.get(url)
    result = response.json()['results']

    for message in result:
        assert message['author'] == auth_user.user.id

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_non_exist_message(django_db_setup, auth_user):
    url = reverse('message-detail', args=[1337])
    response = auth_user.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_foreign_message(django_db_setup, auth_user):
    other_client = get_auth_user()
    ticket = post_ticket('some title', other_client, 201)
    message = post_message('some text', ticket['id'], other_client, 201)

    url = reverse('message-detail', args=[message['id']])
    response = auth_user.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_change_message_ticket_to_foreign(django_db_setup, auth_user):
    other_ticket = post_ticket('some title', get_auth_user(), 201)
    ticket = post_ticket('some title', auth_user, 201)
    message = post_message('some text', ticket['id'], auth_user, 201)

    url = reverse('message-detail', args=[message['id']])
    response = auth_user.put(url, data={'ticket': other_ticket['id']})
    assert response.status_code == 400
