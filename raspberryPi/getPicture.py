import RPi.GPIO as GPIO
import time
import datetime as dt
import time
import picamera
import boto3


def getDistance():
    fDistance = 0.0
    nStartTime, nEndTime = 0, 0

    GPIO.output(TP, GPIO.HIGH)
    usleep(2)
    GPIO.output(TP, GPIO.LOW)
    usleep(10)
    
    while (GPIO.input(EP) == GPIO.LOW):
        pass
    nStartTime = dt.datetime.now()
    while (GPIO.input(EP) == GPIO.HIGH):
        pass
    nEndTime = dt.datetime.now()

    fDistance = (nEndTime - nStartTime).microseconds /29. / 2.
    return fDistance


def takePicture(count):
    with picamera.PiCamera() as camera:
        name = str(count)+'img_user0.jpg'
        camera.capture(name)
    return name

def s3Upload(image):
    try:
        s3.upload_file(image, bucket_name, str('image_sources/') + image)
    except Exception:
        print("error")




GPIO.setmode(GPIO.BCM)

# microwave setup
TP = 4
EP = 17

GPIO.setup(TP, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(EP, GPIO.IN)
time.sleep(0.5)

usleep = lambda x : time.sleep(x/1000000.0)
s3 = boto3.client(
    's3',
    region_name='ap-northeast-2',
    aws_access_key_id='AKIARDTNSHAUQFPQX6FI',
    aws_secret_access_key='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'
    )

bucket_name = 'garbage-recycle'


count = 0

# loop forever
while(True):   
    fDistance = getDistance()
    print(fDistance)
    
    time.sleep(1)

    if fDistance < 30 :
        for i in range(5):
            image = takePicture(count)
            s3Upload(image)
            count += 1
            time.sleep(1)
    elif fDistance < 50 :
        for i in range(2):
            image = takePicture(count)
            s3Upload(image)
            count += 1
            time.sleep(2.5)
    else :
        image = takePicture(count)
        s3Upload(image)
        count += 1
        time.sleep(5)

GPIO.cleanup()




