
# encoding:utf-8

import requests
import base64

'''
通用文字识别（高精度版）
'''

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
# 二进制方式打开图片文件
f = open('temp.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = '24.e718f603d2cde348f06a4d8002af66cb.2592000.1691550523.282335-35955705'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())