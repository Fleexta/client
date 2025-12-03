#  Copyright (c) 2025 Timofei Kirsanov

import json

import requests
from PyQt6.QtCore import QUrl, QEventLoop, QByteArray, pyqtSignal, QObject
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest

url = "http://localhost:8001"
SUPPORT_URL = "http://localhost:8001/docs"
NETLOC = "localhost:8001"


def get(path: str):
    return QUrl(url + path)


def get_common(path: str):
    return url + path


def get_my_chats(token: str):
    request = QNetworkRequest(get("/chats"))
    request.setRawHeader(b"Authorization", f"Bearer {token}".encode("utf-8"))

    manager = QNetworkAccessManager()
    loop = QEventLoop()

    response_data = {}

    def on_finished(reply):
        if reply.error() == reply.NetworkError.NoError:
            response_data['result'] = reply.readAll().data().decode()
        else:
            response_data['result'] = reply.errorString()
        loop.quit()

    manager.finished.connect(on_finished)
    manager.get(request)

    loop.exec()

    return response_data.get('result')


def post_token(path: str, form_data: dict):
    request = QNetworkRequest(get(path))
    request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/x-www-form-urlencoded")

    data = QByteArray()
    for key, value in form_data.items():
        if data:
            data.append(b"&")
        data.append(f"{key}={value}".encode())

    manager = QNetworkAccessManager()
    loop = QEventLoop()
    response = {}

    def finished(reply):
        http_status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        if reply.error() == reply.NetworkError.NoError:
            response['result'] = reply.readAll().data().decode()
        else:
            response['result'] = reply.errorString()
        response['http_status'] = http_status
        loop.quit()

    manager.finished.connect(finished)
    manager.post(request, data)

    loop.exec()

    return response.get('result'), response.get('http_status')


def send_msg(data_dict: dict, chat: int, token: str):
    json_str = json.dumps(data_dict, ensure_ascii=False)

    json_bytes = json_str.encode("utf-8")

    request = QNetworkRequest(get(f"/c/{chat}/send"))
    request.setRawHeader(b"Authorization", f"Bearer {token}".encode())
    request.setRawHeader(b"Content-Type", b"application/json")

    manager = QNetworkAccessManager()
    loop = QEventLoop()
    response = {}

    def finished(reply):
        body = reply.readAll().data().decode()
        if reply.error() == reply.NetworkError.NoError:
            response['result'] = body
        else:
            response['result'] = reply.errorString()
        loop.quit()

    manager.finished.connect(finished)
    manager.post(request, json_bytes)
    loop.exec()
    return response.get('result')


def connect_sse_generator(path, token):
    headers = {
        "Accept": "text/event-stream",
        "Authorization": "Bearer " + token
    }
    try:
        with requests.get(get_common(path), headers=headers, stream=True, timeout=10) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if not decoded_line.strip().startswith(':'):
                        yield decoded_line, response.status_code
    except requests.exceptions.RequestException as e:
        yield f"ERROR: {e}"


class SseWorker(QObject):
    data_received = pyqtSignal(tuple)
    finished = pyqtSignal()

    def __init__(self, url, token):
        super().__init__()
        self.url = url
        self.token = token
        self._running = True

    def run(self):
        for line, status in connect_sse_generator(self.url, self.token):
            if not self._running:
                break

            self.data_received.emit((line, status))

        self.finished.emit()

    def stop(self):
        self._running = False

