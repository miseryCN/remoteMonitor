
"""
监控服务端，运行在有独立IP的服务器上
服务端主要采用flask，搭建一个web服务器，运行3个线程

线程1: 接收被监控端的心跳包，传输图片  端口 1024
线程2: 开启web服务器，实现网页上的图片显示功能  端口 1025
线程3: 接收客户端的心跳包，发送图片到客户端  端口 1026

"""

import threading
from flask import Flask, request, send_file, jsonify
from base64 import b64decode
from datetime import datetime
from time import sleep
import configparser
import os

Config = configparser.ConfigParser()
Config.read("config.ini")


be_monitor = Flask(__name__)
show = Flask(__name__)
monitor_client = Flask(__name__)
isConnect = False
name = None


def be_monitor_func():
    @be_monitor.route('/',methods=['GET','POST'])
    def be_monitor_index():
        data = request.form
        if data['transferType'] == 'sendImage':
            image = b64decode(data['image'])
            global name
            name = datetime.now().strftime('%Y%m%d%H%M%S%f')+'.jpg'
            open('static/'+name, 'wb').write(image)
            global isConnect
            isConnect = False

        if isConnect:
            return 'screenShot'
        else:
            return 'heartBeat'

    be_monitor.run(host='0.0.0.0', port=Config.get('server', 'port1'))


def show_func():
    @show.route('/screenshot', methods=['GET', 'POST'])
    def show_index():
        old_name = name
        global isConnect
        isConnect = True
        flag = True
        count = 0
        while flag:
            if old_name != name:
                flag = False
            sleep(0.1)
            count+=1
            if count == 50:
                return jsonify({"name":"404.jpg"})
        return jsonify({"name":name})

    @show.route('/', methods=['GET', 'POST'])
    def index():
        return send_file("./public/index.html")
    show.run(host='0.0.0.0', port=Config.get('server', 'port2'))


if __name__ == '__main__':
    if not os.path.exists('./static/'):
        os.makedirs('./static/')
    threading.Thread(target=be_monitor_func).start()
    threading.Thread(target=show_func).start()