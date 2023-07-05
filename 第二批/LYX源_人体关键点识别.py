# encoding:utf-8
import time
import requests
import base64
import cv2  # pip install opencv-python
import threading


# cv2图片转base64文本
def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


# 登录百度AI应用账号
def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
    ak, sk)
    response = requests.get(host)  # 访问网址
    return response.json()['access_token']


# 调用百度AI解析人体关键点图片
def analysis_pose(image_np, access_token):
    params = {"image": image_to_base64(image_np)}
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    return response.json()


# 绘制结果到图像上
def draw_person(image, json):
    ss = 0.4  # 显示点的置信度阈值
    lines = [  # 需要绘制的连线列表
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
            for i in range(len(ks)-1):
                v1, v2 = bp[ks[i]], bp[ks[i+1]]
                c1, c2 = (int(v1['x']), int(v1['y'])), (int(v2['x']), int(v2['y']))
                if v1['score'] > ss and v2['score'] > ss:  # 当两个点都存在时绘制中间的连线
                    cv2.line(image, c1, c2, (255, 120, 120), 3)  # 绘制中间连线
        for k in bp:  # 循环绘制每一个点
            v = bp[k]
            if v['score'] > ss:
                c = (int(v['x']), int(v['y']))
                cv2.circle(image, c, 5, (120, 255, 120), -1)  # 绘制一个点
    return image


# 程序从这里开始运行

# 登录百度AI， ak sk 在应用列表获取
ak = '0XWU2LjEjSYAoTEUGXGLZifY'
sk = 'uq06vCyy4Bgjj68Y7KaGvVyOa5bvICx8'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token
print('Token:', token)

cap = cv2.VideoCapture(0)  # 打开电脑摄像头 0指第一个
t = time.time()  # 记录开始运行的时间
result = None  # 记录识别结果


def update(frame):
    global result
    result = analysis_pose(frame, token)  # 通过百度云获取结果
    # print(result)  # 输出结果
    bp = result['person_info'][0]['body_parts']
    
    rwx = bp['right_wrist']['x']
    rwy = bp['right_wrist']['y']
    lwx = bp['left_wrist']['x']
    lwy = bp['left_wrist']['y']

    lsx = bp['left_shoulder']['x']
    lsy = bp['left_shoulder']['y']
    rsx = bp['right_shoulder']['x']
    rsy = bp['right_shoulder']['y']
    
    rhx = bp['right_hip']['x']
    rhy = bp['right_hip']['y']
    lhx = bp['left_hip']['x']
    lhy = bp['left_hip']['y']

    if lwx == lsx:
        lwx += 0.001
    if rwx == rwy:
        rwx += 0.001
    k1 = (lwy - lsy) / (lwx - lsx)
    k2 = (rwy - rsy) / (rwx - rsx)
    d1 = abs(rsx - lsx)
    d2 = abs(rwx - lwx)
    # print(k1, k2, d1, d2)
    # print(lwx, rsx, lwy, rsy)
    # print(rwx > lsx, rwy < lsy, lsx > lhx, lsy < lhy)
    if abs(k1) < 0.3 and abs(k2) < 0.3 and d2 > d1 * 3:
        print('# 检测到伸展运动')
    elif rwx > lsx > lhx and rwy < lsy < lhy:
        print('# 检测到体测运动2')
    elif (k1 > 3 or k1 < -3) and (k1 > 3 or k2 < -3) and lwy > lsy > rwy:
        print('# 检测到体侧运动1')
    else:
        print('检测中...')


while cv2.waitKey(100) < 0:  # 循环不断运行
    hasFrame, frame = cap.read()  # 获取摄像头画面
    if not hasFrame:  # 如果没有图像 跳过
        break

    if time.time() - t > 0.6:  # 每隔0.6秒更新画面
        threading.Thread(target=update, args=(frame,)).start()
        t = time.time()  # 更新结果时间
    if result:
        draw_person(frame, result)  # 绘制结果到图像

    cv2.imshow("POSE", frame)  # 显示运行结
