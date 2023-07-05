import socket
from threading import Thread

from utils import *

upload = {'num': 0}
port = 8003



def handle_client(client_socket):
    request_data = client_socket.recv(1024)
    # print("Request data:", request_data)
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: Server\r\n"
    response_body = str(upload['num'])
    response = response_start_line + response_headers + "\r\n" + response_body
    # 向客户端返回响应数据
    client_socket.send(bytes(response, "utf-8"))
    # 关闭客户端连接
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(128)
    while True:
        client_socket, client_address = server_socket.accept()
        # print("[%s, %s] 用户查询当前人数" % client_address)
        Thread(target=handle_client, args=(client_socket,)).start()


def start_detect(token):
    path = './temp.jpg'
    while True:
        print('准备拍照')
        take_photo(path)  # 拍照
        print('拍照成功')
        img = image_base64(path)

        num = detect_person(img, token)
        upload['num'] = num
        if num == 0:
            print("当前范围内无人")
            led.value(0)
        elif num >= 3:
            print("当前范围内拥挤:", num)
            led.value(1)
            speech('人数较多，请注意安全，避免拥挤。')
        else:
            print("当前范围内有人:", num)
            led.value(1)


def detect_person(img, token):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis" + \
          "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {"image": img}
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    num = 0
    for p in result['person_info']:
        if p['location']['score'] > 0.8:
            num += 1
    return num


if __name__ == '__main__':
    # 启动人数查询服务端线程
    Thread(target=start_server).start()

    token = get_token("0XWU2LjEjSYAoTEUGXGLZifY", "uq06vCyy4Bgjj68Y7KaGvVyOa5bvICx8")
    # token = '24.03616e3bc6099875ca4987ab08019d14.2592000.1645504336.282335-25546667'
    print('Token: ' + token)

    start_detect(token)
