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
    pword = input("请输入一句话:")
    payload = urlencode({"text": pword})
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        sword = response.json()[
            "data"][0]["hits"][0]["wordHitPositions"][0]["keyword"]

        print("检测到敏感文本:  "+sword)
        lens = len(sword)
        a = pword.replace(sword, "*"*lens)
        print("替换后的文本:  "+a)
    except:
        print("该文本没有网络暴力词汇")


if __name__ == '__main__':
    main()
