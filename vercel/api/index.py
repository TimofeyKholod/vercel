from http.server import BaseHTTPRequestHandler
from flask import Flask, jsonify
import sys
import os

# Добавляем путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Создаем Flask приложение
app = Flask(__name__)
@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!"})


@app.route('/api/users')
def users():
    return jsonify({"users": ["John", "Jane", "Bob"]})


# Адаптер для Vercel
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from io import BytesIO
        from flask import Request, Response
        import json

        # Создаем Flask request из HTTP request
        body = b''
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length:
            body = self.rfile.read(content_length)

        environ = {
            'REQUEST_METHOD': self.command,
            'PATH_INFO': self.path,
            'QUERY_STRING': self.requestline.split('?', 1)[1] if '?' in self.requestline else '',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }

        # Запускаем Flask приложение
        with app.app_context():
            response = app(environ, lambda status, headers: None)

        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b''.join(response))
