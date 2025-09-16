import pytest
from unittest.mock import patch, MagicMock
from servidor import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("servidor.connect_db")
def test_listar_todos_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "Rua A", "Rua", "Bairro A", "Cidade A", "00000-000", "casa", 100000.0, "2020-01-01")
    ]
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis")
    assert response.status_code == 200
    assert response.get_json()["imoveis"][0]["logradouro"] == "Rua A"

@patch("servidor.connect_db")
def test_listar_imovel_por_id(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, "Rua A", "Rua", "Bairro A", "Cidade A", "00000-000", "casa", 100000.0, "2020-01-01"
    )
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis/1")
    assert response.status_code == 200
    assert response.get_json()["logradouro"] == "Rua A"

@patch("servidor.connect_db")
def test_adicionar_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 1  # Adicionado para corrigir o erro!
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

    expected_response = novo.copy()
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
    esperado = atualizado.copy()
    esperado["id"] = 1
    assert response.get_json() == esperado

@patch("servidor.connect_db")
def test_remover_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    response = client.delete("/imoveis/1")
    assert response.status_code == 204
    assert response.get_data(as_text=True) == ""

@patch("servidor.connect_db")
def test_listar_por_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "Rua X", "Avenida", "Bairro X", "Cidade X", "11111-111", "casa", 250000.0, "2019-06-20")
    ]
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis/tipo/casa")
    assert response.status_code == 200
    assert response.get_json()["imoveis"][0]["tipo"] == "casa"

@patch("servidor.connect_db")
def test_listar_por_cidade(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (2, "Rua Y", "Rua", "Bairro Y", "São Paulo", "22222-222", "apartamento", 300000.0, "2022-08-10")
    ]
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis/cidade/São Paulo")
    assert response.status_code == 200
    assert response.get_json()["imoveis"][0]["cidade"] == "São Paulo"