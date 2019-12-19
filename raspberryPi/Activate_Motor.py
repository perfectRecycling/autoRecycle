import RPi.GPIO as GPIO
from time import sleep

import paho.mqtt.client as mqtt


GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
p1= GPIO.PWM(38,50)
p2= GPIO.PWM(13,50)
p3= GPIO.PWM(16,50)
p4= GPIO.PWM(40,50)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

val = 3
while(1):
    def on_connect(client, userdata, flags, rc):
        print("Connect")
        client.subscribe("user/0")

    def on_message(client, userdata, msg):
        myMessage = str(msg.payload)
        print(myMessage)
        
        flag = [0,0,0,0]
        if(myMessage.find("paper") != -1):
            p1.ChangeDutyCycle(5)
            flag[0] = 1
        if(myMessage.find("plastic") != -1):
            p2.ChangeDutyCycle(4.5)
            flag[1] = 1
        if(myMessage.find("glass") != -1):
            p3.ChangeDutyCycle(4.5)
            flag[2] = 1
        if(myMessage.find("metal") != -1):
            p4.ChangeDutyCycle(5.2)
            flag[3] = 1
        sleep(5)
        if(flag[0] == 1):
            p1.ChangeDutyCycle(25)
        if(flag[1] == 1):
            p2.ChangeDutyCycle(25)
        if(flag[2] == 1):
            p3.ChangeDutyCycle(25)
        if(flag[3] == 1):
            p4.ChangeDutyCycle(25)
        

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)
    client.loop_forever()
    sleep(3)

p.stop()
GPIO.cleanup()
