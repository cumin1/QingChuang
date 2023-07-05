import time

import requests
import base64
import cv2
import threading
import math


def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    response = requests.get(host)
    return response.json()['access_token']


def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


def analysis_pose(image_np, access_token):
    params = {"image": image_to_base64(image_np)}
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    return response.json()


def draw_person(image, json):
    ss = 0.4
    lines = [
        'left_ear,left_eye,nose,right_eye,right_ear',
        'left_wrist,left_elbow,left_shoulder,neck,right_shoulder,right_elbow,right_wrist',
        'nose,neck',
        'left_hip,right_hip',
        'left_shoulder,left_hip,left_knee,left_ankle',
        'right_shoulder,right_hip,right_knee,right_ankle',
    ]
    for info in json['person_info']:  # 循环绘制每一个人
        bp = info['body_parts']
        for l in lines:
            ks = l.split(',')
            for i in range(len(ks) - 1):
                v1, v2 = bp[ks[i]], bp[ks[i + 1]]
                c1, c2 = (int(v1['x']), int(v1['y'])), (int(v2['x']), int(v2['y']))
                if v1['score'] > ss and v2['score'] > ss:  # 当两个点都存在时绘制中间的连线
                    cv2.line(image, c1, c2, (255, 120, 120), 3)  # 绘制中间连线
        for k in bp:  # 循环绘制每一个点
            v = bp[k]
            if v['score'] > ss:
                c = (int(v['x']), int(v['y']))
                cv2.circle(image, c, 5, (120, 255, 120), -1)  # 绘制一个点
    return image


def dis(p1, p2):
    return math.sqrt((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2)


def check(arr):
    for p in arr:
        if p['score'] < 0.2:
            return False
    return True


def update(frame):
    global result
    result = analysis_pose(frame, token)  # 通过百度云获取结果
    bp = result['person_info'][0]['body_parts']
    lw = bp['left_wrist']
    rw = bp['right_wrist']
    th = bp['top_head']
    lh = bp['left_hip']
    rh = bp['right_hip']
    lk = bp['left_knee']
    rk = bp['right_knee']

    print(dis(lw, th), dis(rw, th))
    if check([lw, rw, th, lh]) and dis(lw, th) < 200 and dis(rw, th) < 200:
        print('检测到抱头动作')
    if check([lh, lk, rh, rk]) and dis(lh, lk) < 400 and dis(rh, rk) < 400:
        print('检测到蹲下动作')
    if check([lw, rw, th, lh, rh, rk]) and dis(lw, th) < 200 and dis(rw, th) < 200 and 400 and dis(rh, rk) < 400:
        print('检测到蹲下抱头动作')


# 程序从这里开始运行

# 登录百度AI， ak sk 在应用列表获取
ak = '0XWU2LjEjSYAoTEUGXGLZifY'
sk = 'uq06vCyy4Bgjj68Y7KaGvVyOa5bvICx8'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token
print('Token:', token)

cap = cv2.VideoCapture(0)  # 打开电脑摄像头 0指第一个
t = time.time()  # 记录开始运行的时间
result = None  # 记录识别结果

while cv2.waitKey(100) < 0:  # 循环不断运行
    hasFrame, frame = cap.read()  # 获取摄像头画面
    if not hasFrame:  # 如果没有图像 跳过
        break

    if time.time() - t > 1:  # 每隔0.6秒更新画面
        threading.Thread(target=update, args=(frame,)).start()
        t = time.time()  # 更新结果时间
    if result:
        draw_person(frame, result)  # 绘制结果到图像

    cv2.imshow("POSE", frame)  # 显示运行结果
