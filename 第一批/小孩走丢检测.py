# coding=utf-8
import base64
import json

import requests
from picamera import PiCamera
import base64
import time


# 照相函数
def take_photo(path):
    camera = PiCamera()  # 定义一个摄像头对象
    camera.resolution = (1024, 768)  # 摄像界面为1024*768
    camera.start_preview()  # 开始摄像
    time.sleep(2)
    camera.capture(path)  # 拍照并保存
    camera.stop_preview()
    camera.close()


# 对图片的格式进行转换
def image_base64(path):
    f = open(path, 'rb')
    image = base64.b64encode(f.read())
    return image


# Baidu token
def get_token(api_key, secret_key):
    host = 'https://aip.baidubce.com/oauth/2.0/token' \
           '?grant_type=client_credentials' \
           '&client_id=' + api_key + \
           '&client_secret=' + secret_key
    response = requests.get(host)
    if response:
        return response.json()["access_token"]
    else:
        return ""


# Baidu interface request
def bd_request(img, token, interface, data={}):
    url = "https://aip.baidubce.com/rest/2.0/%s?access_token=%s" % (interface, token)
    headers = {'content-type': 'application/json'}
    data['image'] = img.decode()
    data['image_type'] = 'BASE64'
    data['max_face_num'] = 120
    data = json.dumps(data)
    # print(data)
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    return result


def search(img, token, group_id):
    data = {'group_id_list': group_id}
    result = bd_request(img, token, 'face/v3/search', data)
    return result


def detect(img, token):
    data = {
        "image": "image",
        "image_type": "BASE64",
        "face_field": "age",
    }
    result = bd_request(img, token, 'face/v3/detect', data)
    return result


if __name__ == '__main__':
    token = get_token("vUPjNRWaolnV9adZ0Mmqbjpy", "ZEvoPWqmsCoohzcPx6npBNjUPrs5U2FX")
    print('Token: ' + token)

    path = "./temp.jpg"

    while True:
        take_photo(path)
        img = image_base64(path)

        result = detect(img, token)['result']
        had_child = False
        had_adult = False
        if result is not None:
            for face in result['face_list']:
                print(face)
                age = face['age']
                if age <= 20:
                    had_child = True
                elif age >= 20:
                    had_adult = True
        if had_child and not had_adult:
            print('有小孩独处')
            result = search(img, token, 'FaceGroup1')
            print(result)
            if result['error_code'] == 0:
                face = result['result']['user_list'][0]
                name = face['user_id']
                if face['score'] > 70:
                    print("人脸识别结果为: " + name)
                else:
                    print('该人脸在人脸库中不存在')
        elif had_child:
            print('有大人陪同小孩')
        else:
            print('摄像头范围内无小孩')
