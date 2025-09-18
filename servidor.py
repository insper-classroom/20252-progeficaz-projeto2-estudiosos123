from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv('.cred')

config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "db_imobiliaria"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "ssl_ca": os.getenv("SSL_CA_PATH")
}

def connect_db():
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro: {e}")
        return None

app = Flask(__name__)

def row_to_dict(row):
    return {
        "id": row[0],
        "logradouro": row[1],
        "tipo_logradouro": row[2],
        "bairro": row[3],
        "cidade": row[4],
        "cep": row[5],
        "tipo": row[6],
        "valor": row[7],
        "data_aquisicao": row[8],
    }

@app.route("/")
def index():
    return jsonify({"msg": "API Imobiliária rodando"}), 200

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conn = connect_db()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco"}), 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()
    conn.close()
    imoveis = [row_to_dict(r) for r in rows]
    return jsonify({"imoveis": imoveis}), 200

@app.route("/imoveis/<int:imovel_id>", methods=["GET"])
def listar_imovel_por_id(imovel_id):
    conn = connect_db()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco"}), 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(row_to_dict(row)), 200
    else:
        return jsonify({"erro": "Imóvel não encontrado"}), 404

@app.route("/imoveis", methods=["POST"])
def adicionar_imovel():
    dados = request.get_json()
    conn = connect_db()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco"}), 500
    cursor = conn.cursor()
    sql = """INSERT INTO imoveis
             (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    valores = (
        dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"],
        dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"]
    )
    cursor.execute(sql, valores)
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    resposta = dados.copy()
    resposta["id"] = novo_id
    return jsonify(resposta), 201

@app.route("/imoveis/<int:imovel_id>", methods=["PUT"])
def atualizar_imovel(imovel_id):
    dados = request.get_json()
    conn = connect_db()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco"}), 500
    cursor = conn.cursor()
    sql = """UPDATE imoveis
             SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s,
                 cep=%s, tipo=%s, valor=%s, data_aquisicao=%s
             WHERE id=%s"""
    valores = (
        dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"],
        dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"], imovel_id
    )
    cursor.execute(sql, valores)
    conn.commit()
    conn.close()
    dados["id"] = imovel_id
    return jsonify(dados), 200

@app.route("/imoveis/<int:imovel_id>", methods=["DELETE"])
def remover_imovel(imovel_id):
    conn = connect_db()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco"}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id=%s", (imovel_id,))
    conn.commit()
    conn.close()
    return "", 204

@app.route("/imoveis/tipo/<string:tipo>", methods=["GET"])
def listar_por_tipo(tipo):
    conn = connect_db()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco"}), 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    rows = cursor.fetchall()
    conn.close()
    imoveis = [row_to_dict(r) for r in rows]
    return jsonify({"imoveis": imoveis}), 200

@app.route("/imoveis/cidade/<string:cidade>", methods=["GET"])
def listar_por_cidade(cidade):
    conn = connect_db()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco"}), 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    rows = cursor.fetchall()
    conn.close()
    imoveis = [row_to_dict(r) for r in rows]
    return jsonify({"imoveis": imoveis}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5500)