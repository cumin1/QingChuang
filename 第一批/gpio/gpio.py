import time
from pinpong.board import Board,Pin

Board("RPi").begin()               #初始化，选择板型(uno、microbit、RPi、handpy)和端口号，不输入端口号则进行自动识别
#Board("uno","COM36").begin()      #windows下指定端口初始化
#Board("uno","/dev/ttyACM0").begin() #linux下指定端口初始化
#Board("uno","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化


led = Pin(Pin.D16, Pin.OUT) #引脚初始化为电平输出

while True:
  #led.value(1) #输出高电平 方法1
  led.write_digital(1) #输出高电平 方法2
  print("1") #终端打印信息
  time.sleep(1) #等待1秒 保持状态

  #led.value(0) #输出低电平 方法1
  led.write_digital(0) #输出低电平 方法2
  print("0") #终端打印信息
  time.sleep(1) #等待1秒 保持状态
