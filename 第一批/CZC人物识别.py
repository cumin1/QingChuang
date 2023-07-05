from utils import *


def detect_person(img, token):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis" + \
          "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {"image": img}
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    print(result)
    num = result['person_num']
    return num


if __name__ == '__main__':
    token = get_token("0XWU2LjEjSYAoTEUGXGLZifY", "uq06vCyy4Bgjj68Y7KaGvVyOa5bvICx8")
    # token = '24.03616e3bc6099875ca4987ab08019d14.2592000.1645504336.282335-25546667'
    print('Token: ' + token)

    while True:
        print('准备拍照')
        path = 'temp.jpg'
        take_photo(path)  # 拍照
        print('拍照成功')
        img = image_base64(path)

        num = detect_person(img, token)
        print('检测到人数: ', num)

        if num > 0:
            led1.value(1)
            led2.value(0)
            speech('有行人过马路，请停车等待。')
        else:
            led1.value(0)
            led2.value(1)
