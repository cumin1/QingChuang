from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import requests
import json
import base64
import time

camera = PiCamera()  # 定义一个摄像头对象


# 照相函数
def getImage():
    camera.resolution = (1024, 768)  # 摄像界面为1024*768
    camera.start_preview()  # 开始摄像
    time.sleep(2)
    camera.capture('faceImage.jpg')  # 拍照并保存
    time.sleep(2)


# 对图片的格式进行转换
def transImage():
    f = open('faceImage.jpg', 'rb')
    image = base64.b64encode(f.read())
    return image


# 上传到百度api进行人脸检测
def go_api(image):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"

    access_token = '24.03616e3bc6099875ca4987ab08019d14.2592000.1645504336.282335-25546667'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}

    req_data = json.dumps(
        {'image': image.decode(), 'image_type': 'BASE64', 'group_id_list': 'FaceGroup1', 'quality_control': 'LOW',
         'liveness_control': 'NORMAL'})
    result = requests.post(request_url, data=req_data, headers=headers)
    result = result.json()

    if result['result'] is not None:
        name = result['result']['user_list'][0]['user_id']  # 获取名字
        score = result['result']['user_list'][0]['score']  # 获取相似度
        if score > 80:  # 如果相似度大于80
            print("你是" + name)
        else:
            print("未找到相关信息")
            return 0
        curTime = time.asctime(time.localtime(time.time()))  # 获取当前时间

        # 将识别记录保存到log.txt中
        f = open('log.txt', 'a')
        f.write("Person: " + name + ";" + "Time:" + str(curTime) + '\n')
        f.close()
        return 1
    # if result.json()['error_msg'] == 'pic not has face':
    #     print('检测不到人脸')
    #     time.sleep(2)
    #     return 0
    else:
        print(result)
        return 0


if __name__ == '__main__':
    print('准备')
    getImage()  # 拍照
    img = transImage()  # 转换照片格式
    res = go_api(img)  # 将转换了格式的图片上传到百度云
    if res == 1:  # 是人脸库中的人
        print("识别成功")
    else:
        print("识别失败")
    camera.stop_preview()
    camera.close()
