#!/usr/bin/env python
"""
================================================
ABElectronics Servo Pi pwm controller | PWM servo controller demo
run with: python demo_servomove.py
================================================
This demo shows how to set the limits of movement on a servo
and then move between those positions

mapping for my boars:
    Library_channel | HAT_pwm_out
                1   |   0
                2   |   1
                15  |   14
                16  |   15  (not in use)
"""

import time

try:
    from driver.ServoPi import Servo
except ImportError:
    print("Failed to import ServoPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys

        sys.path.append("..")
        from ServoPi import Servo
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    """
    Main program function
    """
    # create an instance of the servo class on I2C address 0x40
    servo = Servo(0x6F)  # 0x40)

    yaw = 14
    # set the servo minimum and maximum limits in milliseconds
    # the limits for a servo are typically between 1ms and 2ms.

    servo.set_low_limit(1.0)
    servo.set_high_limit(2.0)

    # Enable the outputs
    servo.output_enable()

    # move the servo across its full range in increments of 10
    try:
        while True:
            for i in range(0, 250, 10):
                servo.move(yaw + 1, i)
                time.sleep(0.1)
                print("servo pos: {}".format(servo.get_position(yaw + 1)))

            for i in range(2, 0, -10):
                servo.move(yaw + 1, i)
            print("moving")

    except KeyboardInterrupt as err:
        servo.output_disable()
        print("output disabled")


if __name__ == "__main__":
    main()
