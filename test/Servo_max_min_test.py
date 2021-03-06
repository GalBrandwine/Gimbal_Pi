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
    roll = 0
    pitch = 1

    # set the servo minimum and maximum limits in milliseconds
    # the limits for a servo are typically between 1ms and 2ms.

    # Yaw can turn 180 deg
    servo.set_low_limit(0.7, yaw)
    servo.set_high_limit(2.4, yaw)

    # roll can turn 90 deg (-45 to +45)
    servo.set_low_limit(1.0, roll)
    servo.set_high_limit(2.0, roll)

    # Pith can turn 90 deg (-45 to +45)
    servo.set_low_limit(1.0, pitch)
    servo.set_high_limit(2.0, pitch)

    # Enable the outputs
    servo.output_enable()

    # move the servo across its full range in increments of 10
    try:
        servo.move(yaw + 1, 120)  # face forward (middle of rotation_range
        print("servo pos: {}".format(servo.get_position(yaw + 1)))

        servo.move(roll + 1, 120)  # face forward (middle of roll)
        print("servo pos: {}".format(servo.get_position(roll + 1)))

        servo.move(pitch + 1, 120)  # face forward (middle of roll)
        print("servo pos: {}".format(servo.get_position(pitch + 1)))

        while True:
            servo.move(pitch + 1, 0)  # face forward (middle of rotation_range
            print("servo pos: {}".format(servo.get_position(pitch + 1)))
            time.sleep(1)

            servo.move(pitch + 1, 120)  # face forward (middle of rotation_range)
            print("servo pos: {}".format(servo.get_position(pitch + 1)))
            time.sleep(1)

            servo.move(pitch + 1, 250)  # face forward (middle of rotation_range
            print("servo pos: {}".format(servo.get_position(pitch + 1)))
            time.sleep(1)

            # for i in range(0, 250, 10):
            #     servo.move(yaw + 1, i)
            #     time.sleep(0.5)
            #     print("servo pos: {}".format(servo.get_position(yaw + 1)))
            #
            # for i in range(2, 0, -10):
            #     servo.move(yaw + 1, i)
            print("moving")
    except KeyboardInterrupt as err:
        servo.sleep()  # stop the timers of the PWM, so no ERRORS corrections on the servo...
        print("\noutput disabled\n")


if __name__ == "__main__":
    main()
