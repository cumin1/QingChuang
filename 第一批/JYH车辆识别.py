from utils import *


def detect_obj(img, token):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general" + \
          "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {"image": img}
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    print(result)
    return result


if __name__ == '__main__':
    token = get_token("r0fMHhGGuR5A5fYicM9R89uE", "lsLxfz1pG5eFtGVlNflIiFzowirKBxVN")
    # token = '24.03616e3bc6099875ca4987ab08019d14.2592000.1645504336.282335-25546667'
    print('Token: ' + token)

    while True:
        waitBtnClick()

        print('准备拍照')
        path = 'temp.jpg'
        take_photo(path)  # 拍照
        print('拍照成功')
        img = image_base64(path)

        results = detect_obj(img, token)
        flag = False
        for result in results['result']:
            if "交通工具" in result['root'] and result['score'] > 0.02:
                flag = True
                break
        if flag:
            led.value(1)
            speech('后方有非机动车，请暂不开门。')
        else:
            led.value(0)
            speech('后方没车，可以开门。')

        print('')


