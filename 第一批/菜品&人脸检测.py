# coding=utf-8
import base64
import time
from picamera import PiCamera

import requests


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
def bd_request(token, interface, data={}):
    url = "https://aip.baidubce.com/rest/2.0/%s?access_token=%s" % (interface, token)
    headers = {'content-type': 'application/json'}
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    return result


def search(img, token, group_id):
    data = {
        'group_id_list': group_id,
        'image': img.decode(),
        'image_type': 'BASE64'
    }
    result = bd_request(token, 'face/v3/search', data)
    return result


def dishRecognize(img, token):
    data = {
        "image": img,
        "top_num": 1,
    }
    result = bd_request(token, 'image-classify/v2/dish', data)['result'][0]
    return result


if __name__ == '__main__':
    token = get_token("r0fMHhGGuR5A5fYicM9R89uE", "lsLxfz1pG5eFtGVlNflIiFzowirKBxVN")
    faceToken = get_token("GgLlf5R0CSW1kUOgmOFCufG0", "d0gAPWcV7OHU425TGkS1qtDmddrbgkLu")
    print('DishToken: ' + token)
    print('FaceToken: ' + faceToken)

    wastes = []

    path = "temp.jpg"

    while True:
        take_photo(path)
        img = image_base64(path)

        meal = None
        face = None

        result = dishRecognize(img, token)
        print(result)
        if result['name'] != '非菜' and float(result['probability']) > 0.5:
            meal = result['name']
            print('检测到菜:', meal)
        else:
            print('摄像头中无菜品')

        if meal:
            result = search(img, faceToken, 'FaceGroup1')
            print(result)
            if result['result'] is not None:
                face = result['result']['user_list'][0]['user_id']
                print('face:',face)
            else:
                print('摄像头中无人脸')

        if meal is not None and face is not None:
            timeStr = time.strftime("%H:%M:%S", time.gmtime(time.time()))
            msg = {
                'people': face,
                'meal': meal,
                'time': timeStr,
            }
            wastes.append(msg)
            print('检测到%s浪费食物，菜名:%s，时间:%s' % (msg['people'], msg['meal'], msg['time']))

        print('')
