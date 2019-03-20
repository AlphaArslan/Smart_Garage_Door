##################### IMPORT #####################
import RPi.GPIO as GPIO
import picamera
import requests
import base64
import json
import time
import os

##################### Global #####################
#constants
PWD         = os.path.dirname(os.path.realpath(__file__))       #returns path to project folder
DB_PATH     = PWD + '/dbfile'
IMAGE_PATH  = PWD + '/tmp.jpg'
api_url     = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=sk_d1f041e7fe7cef9f91f69fad'
plate1      = "plate1"
plate2      = "plate3"
plate3      = "plate3"

# Pin Configuration
LASER    = 11
DETECTOR = 13

################### Funcutions ###################
def wait_for_cars():
    while GPIO.input(DETECTOR) is True:
        print('--- Waiting for cars')
        time.sleep(1)

def check_plates(plate1, plate2, plate3):
    pass

def allowed_fun(p):
    pass

def rejected_fun():
    pass

##################### setup ######################
# setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LASER ,GPIO.OUT)
GPIO.setup(DETECTOR ,GPIO.IN)

######## reading database


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
