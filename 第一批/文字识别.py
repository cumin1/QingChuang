# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:30:45 2021

@author: hwfen
"""

# -*- coding = utf-8 -*-
# @Time : 2021/3/19 9:55
# @Author : 陈良兴
# @File : 文字识别.py
# @Software : PyCharm

import requests
import base64
from aip import AipOcr
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import json
import time

camera = PiCamera()  # 定义一个摄像头对象

APP_ID = '25551695'
API_KEY = 'Me3dqRWrGbp1kxIX5nYtkMg6'
SECRET_KEY = 'WLjqyOwhHhcExTdUXhG7FNIlvS8kksLh'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY


def getToken():
    access_token = ''
    response = requests.get(host)
    if response:
        access_token = response.json()['access_token']
    return access_token


# 照相函数
def getImage():
    camera.resolution = (1024, 768)  # 摄像界面为1024*768
    camera.start_preview()  # 开始摄像
    time.sleep(5)
    camera.capture('text.jpg')  # 拍照并保存
    time.sleep(2)


# 对图片的格式进行转换
def transImage():
    f = open('text.jpg', 'rb')
    image = base64.b64encode(f.read())
    return image


# 把图片里的文字识别出来
def img_to_str(image):
    # 通用文字识别（标准版）
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 通用文字识别（高精度版）
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 网络图片识别
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
    # 二进制方式打开图片文件
    # https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=24.f9ba9c5241b67688bb4adbed8bc91dec.2592000.1485570332.282335-8574074

    params = {"image": image}
    access_token = getToken()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    r = json.loads(response.text)
    return r  # res_words


if __name__ == '__main__':
    print('准备')
    getImage()  # 拍照
    img = transImage()  # 转换照片格式
    res = img_to_str(img)  # 文字识别
    if res['words_result_num'] > 0:
        for i in range(0, res['words_result_num']):
            print(res['words_result'][i]['words'])
    camera.stop_preview()
    camera.close()
