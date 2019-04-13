#!/usr/bin/python

import time

import os
print(os.path.dirname(os.path.abspath(__file__)))

from driver.Raspi_PWM_Servo_Driver import PWM

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x6F)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096


def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length /= 60  # 60 Hz
    print("%d us per period" % pulse_length)
    pulse_length /= 4096  # 12 bits of resolution
    print("%d us per bit" % pulse_length)
    pulse *= 1000
    pulse /= pulse_length
    pwm.set_pwm(channel, 0, pulse)


pwm.set_pwm_freq(60)  # Set frequency to 60 Hz
while True:
    # Change speed of continuous servo on channel O
    pwm.set_pwm(0, 0, servoMin)
    time.sleep(1)
    pwm.set_pwm(0, 0, servoMax)
    time.sleep(1)
