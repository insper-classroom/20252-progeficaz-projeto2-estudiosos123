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
    except Error as err:
        print(f"Erro: {err}")
        return None

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"msg": "API Imobiliária rodando"}), 200


if __name__ == "__main__":
    app.run(debug=True)
