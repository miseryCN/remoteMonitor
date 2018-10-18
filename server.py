
"""
监控服务端，运行在有独立IP的服务器上
服务端主要采用flask，搭建一个web服务器，运行3个线程

线程1: 接收被监控端的心跳包，传输图片  端口 1024
线程2: 开启web服务器，实现网页上的图片显示功能  端口 1025
线程3: 接收客户端的心跳包，发送图片到客户端  端口 1026

"""

import threading
from flask import Flask,request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    print(request.form['transfer_type'])
    return 'wkm_da_sa_bi'

def run(port):
    app.run(host='0.0.0.0',port=port)

for port in range(1024,1027):
    threading.Thread(target=run,args=(port,)).start()

