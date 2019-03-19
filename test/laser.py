import RPi.GPIO as GPIO
import time


##################### Global #####################
# Pin Configuration
LASER    = 11
DETECTOR = 13


##################### setup ######################
# setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LASER ,GPIO.OUT)
GPIO.setup(DETECTOR ,GPIO.IN)
GPIO.output(LASER, True)

###################### loop ######################
while True :
    if GPIO.input(DETECTOR) is False:
        print("car found")
    else:
        print("no cars")
    time.sleep(1)
