from PIL import ImageGrab
from wmi import WMI
from socketIO_client import SocketIO, LoggingNamespace
from base64 import b64encode
save_path = 'd:/1.jpg'


def get_serial_number():
    bios = WMI().Win32_BIOS()[0]
    board = WMI().Win32_BaseBoard()[0]
    return bios.SerialNumber+board.SerialNumber


def screen_shot(save_path):
    image = ImageGrab.grab()
    image.save(save_path)
    image = b64encode(open(save_path,'rb').read())
    return image


socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)


def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')


def print_screen(data):
    print('请求截图!那么截图!')
    img = screen_shot(save_path)
    socketIO.emit('print_result', {"img": str(img, encoding='utf-8'), "sid": data["sid"], "serial_number": get_serial_number()})


def init(data):
    print('截屏客户端初始化!')
    socketIO.emit('serial_number',{"serial_number": get_serial_number()})


socketIO.on('connect', on_connect)
socketIO.on('init', init)
socketIO.emit('init')
socketIO.on('print', print_screen)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

socketIO.wait()