from aip import AipFace
import base64
import time
from picamera import PiCamera

APP_ID = "25565021"
API_Key = "KbN65GokyRpikyV7rmojIdT7"
Secret_Key = "dlt8NDNOZWGtQuNtNSQN3h93RoYZAizH"
client = AipFace(APP_ID, API_Key, Secret_Key)

groupId = "FaceGroup1"
imageType = "BASE64"

camera = PiCamera()


def get_image():
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(3)
    camera.capture("faceImage.png")
    with open("faceImage.png", "rb") as f:
        image = base64.b64encode(f.read())
    return image.decode()


def get_group_users(group_id_list):
    res = client.getGroupUsers(group_id_list)
    try:
        user_id_list = res["result"]["user_id_list"]
        return user_id_list
    except (KeyError, TypeError):
        print(res)


def search_face(image, image_type, group_id_list):
    res = client.search(image, image_type, group_id_list)

    try:
        user_id = res["result"]["user_list"][0]["user_id"]
        score = res["result"]["user_list"][0]["score"]
        return user_id, score
    except (KeyError, TypeError):
        print(res)


userList = get_group_users(groupId)
onTimeList = []
lateList = []
absentList = userList


def late_judge(image):
    userId, userScore = search_face(image, imageType, groupId)
    deadline = "15:00"

    if (int(time.strftime("%H")) > int(deadline[:2])) or \
            (int(time.strftime("%H")) == int(deadline[:2]) and int(time.strftime("%M")) > int(deadline[3:])):

        if userId not in lateList:
            lateList.append(userId)
            print(f"{userId}，您迟到了！")
        if userId in absentList:
            del absentList[absentList.index(userId)]
    else:

        if userId not in onTimeList:
            onTimeList.append(userId)
            print(f"{userId}，您准时到达！")
        if userId in absentList:
            del absentList[absentList.index(userId)]


def list_output():
    if onTimeList:
        print("准时到达的人有", end="")
        print(*onTimeList, sep="、")
    if lateList:
        print("迟到的人有", end="")
        print(*lateList, sep="、")
    if absentList:
        print("旷课的人有", end="")
        print(*absentList, sep="、")


if __name__ == '__main__':
    ticks = 0
    while True:
        try:
            picture = get_image()
            late_judge(picture)
            ticks += 1
        except KeyboardInterrupt:
            break
    list_output()
