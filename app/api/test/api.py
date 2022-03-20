from rest_framework.reverse import reverse
from rest_framework.test import APIClient


def post_ticket(title: str, client: APIClient, status_code: int):
    url = reverse('ticket-list')
    response = client.post(url, data={'title': title})
    assert response.status_code == status_code
    return response.json()


def post_message(text: str, ticket: int, client: APIClient, status_code: int):
    url = reverse('message-list')
    response = client.post(url, data={'text': text, 'ticket': ticket})
    assert response.status_code == status_code
    return response.json()