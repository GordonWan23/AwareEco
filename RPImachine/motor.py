from time import sleep
import RPi.GPIO as GPIO

def Rotate(D, Deg, Spd):
    if D>=1:
        CW=1
        CCW=0
    if D<=-1:
        CW=0
        CCW=1
    DIR = 20       # Direction GPIO Pin
    STEP = 21      # Step GPIO Pin
    EN = 16
    SPR = int((Deg/360)*200)    # Steps per Revolution (360 / 1.8)
    print(SPR)

    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(EN, GPIO.OUT)
    GPIO.output(EN, GPIO.LOW)
    GPIO.output(DIR, CW)

    MODE = (14, 15, 18)
    # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}

    GPIO.output(MODE, RESOLUTION['1/32'])

    step_count = SPR 
    delay = Spd/334


    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    sleep(.5)
    GPIO.output(DIR, CCW)

    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    return 1

def RotateMono(D, Deg, Spd):
    if D>=1:
        CW=1
        CCW=0
    if D<=-1:
        CW=0
        CCW=1
    DIR = 20       # Direction GPIO Pin
    STEP = 21      # Step GPIO Pin
    SPR = int((Deg/360)*200)    # Steps per Revolution (360 / 1.8)
    print(SPR)

    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CW)

    MODE = (14, 15, 18)
    # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}

    GPIO.output(MODE, RESOLUTION['1/32'])

    step_count = SPR 
    delay = Spd/334


    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    sleep(.5)
    GPIO.output(DIR, CCW)

    return 1

# Rotate(-1,70,5)