##################### IMPORT #####################
import RPi.GPIO as GPIO
import picamera
import requests
import base64
import json
import time
import os

import control_DB

##################### Global #####################
#constants
PWD         = os.path.dirname(os.path.realpath(__file__))       #returns path to project folder
DB_PATH     = 'database.db'
IMAGE_PATH  = PWD + '/tmp.jpg'
api_url     = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=sk_d1f041e7fe7cef9f91f69fad'
plate1      = "plate1"
plate2      = "plate3"
plate3      = "plate3"
DELAY       = 5                                                 # time for servo opening

# Pin Configuration
servo_pin = 11
LASER     = 13
DETECTOR  = 15

################### Funcutions ###################
def wait_for_cars():
    while GPIO.input(DETECTOR) is True:
        print('--- Waiting for cars')
        time.sleep(1)

def check_plates(plate1, plate2, plate3):
    c.execute("SELECT * FROM cars")
    s = c.fetchone()
    while s is not None:
        if s[1] in (plate1, plate2, plate3)
            allowed_fun(s)
            break

def allowed_fun(s):
    print(s[0] + " Car Found")
    # open servo
    servo_angle(90)
    time.sleep(DELAY)
    servo_angle(0)

def servo_angle(angle):
    duty = angle/18 + 2.5
    GPIO.output(servo_pin, True)
    servo_pwm.ChangeDutyCycle(duty)

##################### setup ######################
# setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LASER ,GPIO.OUT)
GPIO.setup(DETECTOR ,GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)
servo_pwm = GPIO.PWM(servo_pin, 50)                 #Servo PWM
servo_pwm.start(0)

######## database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
control_DB.init_db()

###################### loop ######################
while True :
        ######## wait for cars [laser detector]
        wait_for_cars()

        ######## capture the image and save it
        with picamera.PiCamera() as camera:
                camera.resolution = (1280 , 720)
                camera.capture(IMAGE_PATH)
        print("--  Picture token")

        ######## process the image to get plates
        with open(IMAGE_PATH, 'rb') as image_file:
                img_base64 = base64.b64encode(image_file.read())

        print("--  sending image online")
        flag = True
        while flag:
                try:
                        r = requests.post(api_url, data = img_base64)
                except requests.exceptions.ConnectionError:
                        print("XX  Connection lost .. Please reconnect")
                        time.sleep(1)
                else:			#no problem occuered
                        flag = False
                        print("--  Connected .. waiting results")
        r = r.json()

        if (len(r["results"]) == 0):
            print("-   No cars seen")
            continue

        plate1 = r["results"][0]["plate"]
        try:
                plate2 = r["results"][0]["candidates"][1]["plate"]
        except IndexError:
                plate2 = "No_plate"
        try:
                plate3 = r["results"][0]["candidates"][2]["plate"]
        except IndexError:
                plate3 = "No_plate"

        print("-   Plate Guess 1 :" + plate1 )
        print("-   Plate Guess 2 :" + plate2 )
        print("-   Plate Guess 3 :" + plate3 )

        ######## check the plate number
        check_plates(plate1, plate2, plate3)
