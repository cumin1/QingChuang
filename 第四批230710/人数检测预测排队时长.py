import base64
import requests


def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    response = requests.get(host)  # 访问网址
    return response.json()['access_token']


# 登录百度AI， ak sk 在应用列表获取
ak = '7zGaQccBw09TPjPTuzqGwq4Q'
sk = 'v5WfwNYX62tRR1th1mqAXKWlSpnjG0PU'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token
print('Token:', token)


'''
人体检测和属性识别
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"

# 二进制方式打开图片文件
# a项目的检测
f = open('test.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
access_token = token
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    p_num = response.json()["person_num"]
    print("a项目检测到排队人数:", p_num)
    p1_time = int(p_num)*10
    print("游客还需排", p1_time, "分钟的队")

print("*********************************")

# b项目的检测
f = open('test1.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
access_token = token
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    p_num1 = response.json()["person_num"]
    print("b项目检测到排队人数:", p_num1)
    p2_time = int(p_num1)*12
    print("游客还需排", p2_time, "分钟的队")


if p1_time >= p2_time:
    print("经过计算，去游玩b项目的需要花费的时间较少")
else:
    print("经过计算，去游玩a项目的需要花费的时间较少")
