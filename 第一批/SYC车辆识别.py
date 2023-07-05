from utils import *

# 拍照并识别图中交通工具数量
def detect(token):
    print('准备拍照')
    path = 'temp.jpg'
    take_photo(path)  # 拍照
    print('拍照成功')
    img = image_base64(path)

    url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general" + \
          "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {"image": img}
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    print(result)
    num = 0
    for r in result['result']:
        if "交通工具" in r['root']:
            num += 1
    return num


def waitBtnClick():
    while btn.value() == 0:
        time.sleep(0.1)


def task():
    print('检测任务开始')
    waitBtnClick()
    r1 = detect(token)
    print('道路A 检测到车辆:', r1)
    waitBtnClick()
    r2 = detect(token)
    print('道路B 检测到车辆:', r2)

    if r1 == 0 and r2 != 0:
        speech('切换绿灯至道路B')
        led1.value(1)
        led2.value(0)
        led3.value(0)
        led4.value(1)
    if r1 != 0 and r2 == 0:
        speech('切换绿灯至道路A')
        led1.value(0)
        led2.value(1)
        led3.value(1)
        led4.value(0)


if __name__ == '__main__':
    token = get_token("r0fMHhGGuR5A5fYicM9R89uE", "lsLxfz1pG5eFtGVlNflIiFzowirKBxVN")
    print('Token: ' + token)

    led.value(1)
    while True:
        task()
