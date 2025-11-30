#  Copyright (c) 2025 Timofei Kirsanov

import json

from PyQt6.QtCore import QUrl, QEventLoop, QByteArray
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest

url = "http://localhost:8001"
SUPPORT_URL = "http://localhost:8001/docs"
NETLOC = "localhost:8001"


def get(path: str):
    return QUrl(url + path)


def get_common(path: str):
    return url + path


def get_chat(chat: int, token: str):
    request = QNetworkRequest(get(f"/c/{chat}"))
    request.setRawHeader(b"Authorization", f"Bearer {token}".encode("utf-8"))

    manager = QNetworkAccessManager()
    loop = QEventLoop()

    response_data = {}

    def on_finished(reply):
        http_status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        if reply.error() == reply.NetworkError.NoError:
            response_data['result'] = reply.readAll().data().decode()
        else:
            response_data['result'] = reply.errorString()
        response_data['http_status'] = http_status
        loop.quit()

    manager.finished.connect(on_finished)
    manager.get(request)

    loop.exec()

    return response_data.get('result'), response_data.get('http_status')


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
