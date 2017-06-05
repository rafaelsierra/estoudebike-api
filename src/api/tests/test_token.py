from freezegun import freeze_time
import pytest

from django.urls import reverse
from django.core.cache import cache

pytestmark = pytest.mark.django_db


@pytest.fixture
def novo_acesso_uri():
    return reverse('api:novo-acesso')


def test_novo_acesso(client, novo_acesso_uri):
    cache.clear()
    response = client.post(novo_acesso_uri)
    assert 'token' in response.json()
    assert len(response.json().get('token')) == 36


def test_limite_novo_acesso(client, novo_acesso_uri):
    cache.clear()
    # Restricao por hora
    with freeze_time("1986-04-26 00:00:00"):
        for x in range(100):
            response = client.post(novo_acesso_uri)
            assert response.status_code == 200
        response = client.post(novo_acesso_uri)
        response.status_code == 429
    cache.clear()
