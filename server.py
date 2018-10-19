
"""
监控服务端，运行在有独立IP的服务器上
服务端主要采用flask，搭建一个web服务器，运行3个线程

线程1: 接收被监控端的心跳包，传输图片  端口 1024
线程2: 开启web服务器，实现网页上的图片显示功能  端口 1025
线程3: 接收客户端的心跳包，发送图片到客户端  端口 1026

"""

from flask import Flask, render_template,send_file
from flask_socketio import SocketIO,send,emit
import json

config = json.load(open("config.json", encoding='utf-8'))
app = Flask(__name__)
app.config['SECRET_KEY'] = config["server"]["secret"]
socketio = SocketIO(app)


@app.route('/')
def hello():
    return send_file("./public/index.html")


@socketio.on('show')
def show():
    emit('show', {"received": True})


if __name__ == '__main__':
    socketio.run(app)

