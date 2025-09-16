import pytest
from unittest.mock import patch, MagicMock
from servidor import app


@pytest.fixture
def client():
    """Cria um cliente de teste Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("servidor.connect_db")
def test_listar_todos_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Nicole Common", "Travessa", "Lake Danielle", "Judymouth",
         "85184", "casa em condominio", 488423.52, "2017-07-29"),
        (2, "Price Prairie", "Travessa", "Colonton", "North Garyville",
         "93354", "casa em condominio", 260069.89, "2021-11-30")
    ]
    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis")
    assert response.status_code == 200

    expected_response = {
        "imoveis": [
            {
                "id": 1,
                "logradouro": "Nicole Common",
                "tipo_logradouro": "Travessa",
                "bairro": "Lake Danielle",
                "cidade": "Judymouth",
                "cep": "85184",
                "tipo": "casa em condominio",
                "valor": 488423.52,
                "data_aquisicao": "2017-07-29"
            },
            {
                "id": 2,
                "logradouro": "Price Prairie",
                "tipo_logradouro": "Travessa",
                "bairro": "Colonton",
                "cidade": "North Garyville",
                "cep": "93354",
                "tipo": "casa em condominio",
                "valor": 260069.89,
                "data_aquisicao": "2021-11-30"
            }
        ]
    }
    assert response.get_json() == expected_response


@patch("servidor.connect_db")
def test_listar_imovel_por_id(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (
        1, "Nicole Common", "Travessa", "Lake Danielle", "Judymouth",
        "85184", "casa em condominio", 488423.52, "2017-07-29"
    )
    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis/1")
    assert response.status_code == 200

    expected_response = {
        "id": 1,
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Travessa",
        "bairro": "Lake Danielle",
        "cidade": "Judymouth",
        "cep": "85184",
        "tipo": "casa em condominio",
        "valor": 488423.52,
        "data_aquisicao": "2017-07-29"
    }
    assert response.get_json() == expected_response


@patch("servidor.connect_db")
def test_adicionar_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    novo = {
        "logradouro": "Rua Teste",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01000-000",
        "tipo": "apartamento",
        "valor": 123456.78,
        "data_aquisicao": "2025-09-15"
    }

    response = client.post("/imoveis", json=novo)
    assert response.status_code == 201

    expected_response = novo
    expected_response["id"] = 1 
    assert response.get_json() == expected_response


@patch("servidor.connect_db")
def test_atualizar_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    atualizado = {
        "logradouro": "Rua Alterada",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "Rio de Janeiro",
        "cep": "22222-000",
        "tipo": "casa",
        "valor": 999999.99,
        "data_aquisicao": "2025-01-01"
    }

    response = client.put("/imoveis/1", json=atualizado)
    assert response.status_code == 200

    expected_response = atualizado
    expected_response["id"] = 1
    assert response.get_json() == expected_response


@patch("servidor.connect_db")
def test_remover_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    response = client.delete("/imoveis/1")
    assert response.status_code == 204

    expected_response = {}
    assert response.get_json(silent=True) == expected_response


@patch("servidor.connect_db")
def test_listar_por_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Amber Drive", "Travessa", "East Maryview", "West Miranda",
         "99073", "casa", 720614.3, "2020-03-06"),
        (2, "Amber Drive", "Travessa", "East Maryview", "West Miranda",
         "99073", "apartamento", 720614.3, "2020-03-06")
    ]
    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis/tipo/casa")
    assert response.status_code == 200

    expected_response = {
        "imoveis": [
            {
                "id": 1,
                "logradouro": "Amber Drive",
                "tipo_logradouro": "Travessa",
                "bairro": "East Maryview",
                "cidade": "West Miranda",
                "cep": "99073",
                "tipo": "casa",
                "valor": 720614.3,
                "data_aquisicao": "2020-03-06"
            }
        ]
    }
    assert response.get_json() == expected_response


@patch("servidor.connect_db")
def test_listar_por_cidade(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (2, "Price Prairie", "Travessa", "Colonton", "North Garyville",
         "93354", "casa em condominio", 260069.89, "2021-11-30"),
        (1, "Price Prairie", "Travessa", "Colonton", "São Paulo",
         "93354", "casa em condominio", 260069.89, "2021-11-30")
    ]
    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis/cidade/North Garyville")
    assert response.status_code == 200

    expected_response = {
        "imoveis": [
            {
                "id": 2,
                "logradouro": "Price Prairie",
                "tipo_logradouro": "Travessa",
                "bairro": "Colonton",
                "cidade": "North Garyville",
                "cep": "93354",
                "tipo": "casa em condominio",
                "valor": 260069.89,
                "data_aquisicao": "2021-11-30"
            }
        ]
    }
    assert response.get_json() == expected_response
