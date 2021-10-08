
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16


def init():
    # init GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up


def get_input(pin):
    return not GPIO.input(pin)
