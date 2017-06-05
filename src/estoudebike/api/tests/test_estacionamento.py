import json
import pytest
import uuid

from django.contrib.gis.geos import Point
from django.urls import reverse

from .test_token import novo_acesso_uri # NOQA

from bike_auth.models import Token
from estacionamento.models import Parada

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
def paradas_iniciais(client, parada_uri):
    lat = -23.5371
    lng = -46.6401
    avaliacao = 0
    for x in range(0, 115, 2):
        for y in range(0, 83, 2):
            token = Token.objects.get_or_create()[0]
            Parada.objects.create(
                token=token,
                local=Point(lng + (x / 10000.0), lat + (y / 10000.0)),
                avaliacao=avaliacao
            )
            avaliacao = avaliacao + 1 if avaliacao <= 5 else 0


@pytest.fixture
def parada_uri():
    return reverse('api:parada')


@pytest.fixture
def buscar_parada_uri():
    return reverse('api:buscar-parada')


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

    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': '10', 'lng': 30},
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

    response = client.post(
        parada_uri,
        json.dumps({
            'token': token,
            'local': {'lat': -10, 'lng': '18'},
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


def test_encontrar_estacionamento(client, buscar_parada_uri, token, paradas_iniciais):
    luz = {'lat': -23.5329, 'lng': -46.6343}
    response = client.post(
        buscar_parada_uri,
        json.dumps({
            'local': luz,
            'token': token,
        }),
        content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 200
    assert 'results' in data
    assert 'next' in data
    assert 'previous' in data

    parada = data['results'][0]
    assert 'distancia' in parada
    assert 'token' not in parada
    assert 'local' in parada
    assert 'lat' in parada['local']
    assert 'lng' in parada['local']
