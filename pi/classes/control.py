import gpiozero

# Assign Pins #
freq = 100
motor1AGPIO = gpiozero.PWMLED(22, frequency=freq)
motor1BGPIO = gpiozero.PWMLED(27, frequency=freq)
motor2AGPIO = gpiozero.PWMLED(4, frequency=freq)
motor2BGPIO = gpiozero.PWMLED(17, frequency=freq)


class control:
    turnVal = 0
    speedVal = 0

    @staticmethod
    def turn(turnval):
        control.turnVal = turnval
        control.output_gpio()

    @staticmethod
    def speed(speedval):
        control.speedval = speedval
        control.output_gpio()

    @staticmethod
    def output_gpio():
        motor1 = 0
        motor2 = 0

        # Find motors speed from turn and speed
        if control.turnval == 0:
            motor1 = control.speedval
            motor2 = control.speedval
        else:
            motor1 = control.speedval * min(abs(control.turnval + 1), 1)
            motor2 = control.speedval * min(abs(control.turnval - 1), 1)

        # Write motor speeds to GPIO
        if motor1 > 0:
            motor1AGPIO.value = abs(motor1)
            motor1BGPIO.value = 0
        else:
            motor1AGPIO.value = 0
            motor1BGPIO.value = abs(motor1)
        if motor2 > 0:
            motor2AGPIO.value = abs(motor2)
            motor2BGPIO.value = 0
        else:
            motor2AGPIO.value = 0
            motor2BGPIO.value = abs(motor2)
