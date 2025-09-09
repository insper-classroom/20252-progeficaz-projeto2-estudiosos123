from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Servidor está rodando!'


if __name__ == '__main__':
    app.run(debug=True)