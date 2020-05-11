# Fake RPi.GPIO Lib just for development purposes
BOARD = 1
OUT = 1
IN = 1


def setmode(a):
    print(a)


def setup(a, b):
    print(a)


def output(a, b):
    print(a)


def cleanup():
    print('a')


def setwarnings(flag):
    print('False')


def PWM(servo_signal, param):
    print('PWM')


def BCM():
    print('BCM')
