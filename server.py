
"""
监控服务端，运行在有独立IP的服务器上
服务端主要采用flask，搭建一个web服务器，运行3个线程

线程1: 接收被监控端的心跳包，传输图片  端口 1024
线程2: 开启web服务器，实现网页上的图片显示功能  端口 1025
线程3: 接收客户端的心跳包，发送图片到客户端  端口 1026

"""

from flask import Flask, render_template,send_file,request
from flask_socketio import SocketIO,send,emit
from datetime import datetime
from base64 import b64decode
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "wsp"
socketio = SocketIO(app)

clients = {}


@app.route('/')
def hello():
    return send_file("./public/index.html")


@socketio.on('show')
def show():
    emit('show', {"received": True})


@socketio.on('print')
def print_screen(client):
    web_info = {"sid": request.sid}
    print('获取到了web请求指定client:'+client+'截图请求!')
    emit('print', web_info, room=client)


@socketio.on('print_result')
def print_screen_result(result):
    img = b64decode(bytes(result["img"], encoding = "utf8"))
    serial_number = result["serial_number"]
    name = serial_number + datetime.now().strftime('%Y%m%d%H%M%S%f') + '.jpg'
    open('static/' + name, 'wb').write(img)
    emit('print_result', {"name": name}, room=result["sid"])


@socketio.on('serial_number')
def get_serial_number(data):
    print('获取到最新的serial_number!',data)
    clients[request.sid] = data["serial_number"]
    print(clients)


@socketio.on('get_clients')
def get_clients():
    emit('get_clients', clients)


@socketio.on('connect')
def connect():
    print('一个客户端连接了!')


@socketio.on('disconnect')
def disconnect():
    print('一个客户端断开连接了!')


@socketio.on('init')
def init():
    emit('init')


if __name__ == '__main__':
    if not os.path.exists('./static/'):
        os.makedirs('./static/')
    socketio.run(app)

