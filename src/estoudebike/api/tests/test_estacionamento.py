import json
import pytest
import uuid

from django.urls import reverse

from .test_token import novo_acesso_uri # NOQA

pytestmark = pytest.mark.django_db


@pytest.fixture
def foto_deitada():
    return """/9j/4AAQSkZJRgABAQEASABIAAD/2wBDABALDA4MChAODQ4SERATGCgaGBYWGDEjJR0oOjM9PDkz
ODdASFxOQERXRTc4UG1RV19iZ2hnPk1xeXBkeFxlZ2P/2wBDARESEhgVGC8aGi9jQjhCY2NjY2Nj
Y2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2P/wAARCAAKAGQDAREA
AhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEB
AAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AKAAAAAA
AAAAAAAAAAAAAAAAAAAAD//Z"""


@pytest.fixture
def foto_de_pe():
    return """/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsK
CwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQU
FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCABkAAoDAREA
AhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAn/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEB
AAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AKpgAAAA
AAAAAAAAAAAAAAAAAAAAA//Z"""


@pytest.fixture
def foto_gigante():
    return """/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEB
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCCcQAAEDAREA
AhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAr/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEB
AAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AL+AAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAf/Z"""


@pytest.fixture
def parada_uri():
    return reverse('api:parada')


@pytest.fixture # NOQA
def token(client, novo_acesso_uri):
    return client.post(novo_acesso_uri).json()['token']


def test_nova_parada(client, parada_uri, token):
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 201
    assert data['local']['lat'] == -10
    assert data['local']['lng'] == 30
    assert data['avaliacao'] == 4


def test_token_invalido(client, parada_uri, token):
    # Token nao é um UUID valido
    response = client.post(
        parada_uri,
        json.dumps({
            'token': 'token invalido',
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4
        }),
        content_type="application/json"
    )
    assert response.status_code == 400

    # Token é um UUID valido mas nao esta registrado
    response = client.post(
        parada_uri,
        json.dumps({
            'token': str(uuid.uuid4()),
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4
        }),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_latitude_longitude_invalido(client, parada_uri, token):
    #
    # Latitude invalida
    #
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -100, 'lng': 30},
            'avaliacao': 4
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'local' in data

    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': 100, 'lng': 30},
            'avaliacao': 4
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'local' in data

    #
    # Longitude invalida
    #
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 181},
            'avaliacao': 4
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'local' in data

    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': -180.005},
            'avaliacao': 4
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'local' in data


def test_avaliacao_invalida(client, parada_uri, token):
    #
    # Avaliacao com ponto flutuante
    #
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4.4
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'avaliacao' in data

    #
    # Avaliacao muito alta
    #
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 6
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'avaliacao' in data

    #
    # Avaliacao muito baixa
    #
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': -1
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'avaliacao' in data


def test_foto_valida(client, parada_uri, token, foto_deitada):
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4,
            'foto': foto_deitada
        }),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_foto_valida_de_pe(client, parada_uri, token, foto_de_pe):
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4,
            'foto': foto_de_pe
        }),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_foto_valida_gigante(client, parada_uri, token, foto_gigante):
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4,
            'foto': foto_gigante
        }),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_foto_invalida_com_base64_valido(client, parada_uri, token):
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4,
            'foto': "bmFvIMOpIHVtYSBmb3RvCg=="
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'foto' in data


def test_foto_com_base64_invalido(client, parada_uri, token):
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4,
            'foto': "isso aqui nao é uma foto base64"
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'foto' in data


def test_foto_com_base64_invalido_2(client, parada_uri, token):
    """Nesse caso pode dar pau se tiver a palavra base64 nos primeiros 30 caracteres mas nao tiver
    nada depois disso"""
    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': 30},
            'avaliacao': 4,
            'foto': "isso aqui nao é base64"
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert 'foto' in data
