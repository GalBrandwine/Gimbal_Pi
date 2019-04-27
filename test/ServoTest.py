#!/usr/bin/python

import time

#from driver.Raspi_PWM_Servo_Driver import PWM
from driver.ServoPi import Servo

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
#pwm = PWM(0x6F)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

yaw = 14


def main():
    """
    Main program function
    """
    # create an instance of the servo class on I2C address 0x40
    servo = Servo(0x40)

    # set the servo minimum and maximum limits in milliseconds
    # the limits for a servo are typically between 1ms and 2ms.

    servo.set_low_limit(1.0)
    servo.set_high_limit(2.0)

    # Enable the outputs
    servo.output_enable()

    # move the servo across its full range in increments of 10
    while True:
        for i in range(0, 250, 10):
            servo.move(yaw, i)
            time.sleep(0.05)

        for i in range(250, 0, -10):
            servo.move(yaw, i)


if __name__ == "__main__":
    main()

# def set_servo_pulse(channel, pulse):
#     pulse_length = 1000000  # 1,000,000 us per second
#     pulse_length /= 60  # 60 Hz
#     print("%d us per period" % pulse_length)
#     pulse_length /= 4096  # 12 bits of resolution
#     print("%d us per bit" % pulse_length)
#     pulse *= 1000
#     pulse /= pulse_length
#     pwm.set_pwm(channel, 0, pulse)
#
#
# pwm.set_pwm_freq(60)  # Set frequency to 60 Hz
#
# angle = 0
# yaw = 14
#
# while True:
#     # Change speed of continuous servo on channel O
#     duty = angle / 18 + 2
#     set_servo_pulse(yaw, duty)
#     # pwm.set_pwm(yaw, 0, servoMin)
#     # time.sleep(1)
#     # pwm.set_pwm(yaw, 0, servoMax)
#     time.sleep(1)
#     angle = angle + 1
#     print(angle)
