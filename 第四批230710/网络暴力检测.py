import requests
from urllib.parse import urlencode


def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    response = requests.get(host)  # 访问网址
    return response.json()['access_token']


# 登录百度AI， ak sk 在应用列表获取
ak = '4zWtn8Cv9CPGsmi3LNbGP7Yr'
sk = 'nRRCMc2kv2GzwzbwNnVBY3dH0wEUOqiU'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token
print('Token:', token)


def main():
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=" + \
        login_baidu_ai(ak, sk)

    payload = 'text=' + urlencode(input("请输入一句话"))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()
