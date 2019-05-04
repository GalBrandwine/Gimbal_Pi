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


class PantTilt:
    """A project-specific class for my pan tilt mechanizem (NOT AN OOP THING). """

    def __init__(self, yaw, roll, pitch, address=0x6f, ):
        # create an instance of the servo class on I2C address 0x40
        self.servo = Servo(address)  # 0x40)

        self.yaw = yaw = 14
        self.roll = roll = 0
        self.pitch = pitch = 1

        # set the servo minimum and maximum limits in milliseconds
        # the limits for a servo are typically between 1ms and 2ms.

        # Yaw can turn 180 deg
        self.servo.set_low_limit(0.7, yaw+1)
        self.servo.set_high_limit(2.4, yaw+1)

        # roll can turn 90 deg (-45 to +45)
        self.servo.set_low_limit(1.0, roll+1)
        self.servo.set_high_limit(2.0, roll+1)

        # Pith can turn 90 deg (-45 to +45)
        self.servo.set_low_limit(1.0, pitch+1)
        self.servo.set_high_limit(2.0, pitch+1)

    def servo_enable(self, flag):
        # Enable the outputs
        self.servo.output_enable() if flag is True else self.servo.output_disable()


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
    servo.set_low_limit(0.7, yaw+1)
    servo.set_high_limit(2.4, yaw+1)

    # roll can turn 90 deg (-45 to +45)
    servo.set_low_limit(1.0, roll+1)
    servo.set_high_limit(2.0, roll+1)

    # Pith can turn 90 deg (-45 to +45)
    servo.set_low_limit(1.0, pitch+1)
    servo.set_high_limit(2.0, pitch+1)

    # Enable the outputs
    servo.output_enable()

    # move the servo across its full range in increments of 10
    try:
        # angle = 0
        # duty_cycle = angle / 18. + 3
        # servo.move(yaw + 1, duty_cycle)  # face forward (middle of rotation_range
        # print(("for duty angle: {} duty_cicle: {}".format(angle, duty_cycle)))
        # print("servo pos: {}".format(servo.get_position(yaw + 1)))
        # time.sleep(1)
        #
        # angle = 90
        # duty_cycle = angle / 18. + 3
        # servo.move(yaw + 1, duty_cycle)  # face forward (middle of rotation_range
        # print(("for duty angle: {} duty_cicle: {}".format(angle, duty_cycle)))
        # print("servo pos: {}".format(servo.get_position(yaw + 1)))
        # time.sleep(1)

        # servo.move(yaw + 1, 120)  # face forward (middle of rotation_range
        # print("servo pos: {}".format(servo.get_position(yaw + 1)))
        #
        # servo.move(roll + 1, 120)  # face forward (middle of roll)
        # print("servo pos: {}".format(servo.get_position(roll + 1)))
        #
        # servo.move(pitch + 1, 120)  # face forward (middle of roll)
        # print("servo pos: {}".format(servo.get_position(pitch + 1)))
        angle = 0
        while True:
            servo.move(yaw + 1, 0)
            time.sleep(1)

            for i in range(0, 250, 10):
                servo.move(yaw + 1, i)
                print("servo pos: {}".format(servo.get_position(yaw + 1)))
                time.sleep(.5)

            #
            # servo.move(pitch + 1, 0)  # face forward (middle of rotation_range
            # print("servo pos: {}".format(servo.get_position(pitch + 1)))
            # time.sleep(1)
            #
            # servo.move(pitch + 1, 120)  # face forward (middle of rotation_range)
            # print("servo pos: {}".format(servo.get_position(pitch + 1)))
            # time.sleep(1)
            #
            # servo.move(pitch + 1, 250)  # face forward (middle of rotation_range
            # print("servo pos: {}".format(servo.get_position(pitch + 1)))
            # time.sleep(1)

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
