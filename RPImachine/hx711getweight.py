#!/usr/bin/env python3
import pickle
import os

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711

def setup():
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=5, pd_sck_pin=6)
    # Check if we have swap file. If yes that suggest that the program was not
    # terminated proprly (power failure). We load the latest state.
    swap_file_name = 'swap_file.swp'
    if os.path.isfile(swap_file_name):
        with open(swap_file_name, 'rb') as swap_file:
            hx = pickle.load(swap_file)
    return hx
            
def getweight(hx):
    num = hx.get_weight_mean(10)
    if num != False:
        weight = str(int(num)) + 'g'
        return weight
    else:
        weight = '0g'
        return weight

def getweightFreq(hx):
    num = hx.get_weight_mean(5)
    return int(num)

# hx = setup()
# while True :
#     print(getweightFreq(hx))