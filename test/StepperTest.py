#!/usr/bin/python
# import RaspiMotorHAT, Raspi_DCMotor, Raspi_Stepper
import atexit

from driver.Raspi_MotorHAT import RaspiMotorHAT

# create a default object, no changes to I2C address or frequency
mh = RaspiMotorHAT(0x6F)


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(RaspiMotorHAT.RELEASE)
    mh.getMotor(2).run(RaspiMotorHAT.RELEASE)
    mh.getMotor(3).run(RaspiMotorHAT.RELEASE)
    mh.getMotor(4).run(RaspiMotorHAT.RELEASE)


atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
myStepper.setSpeed(30)  # 30 RPM

while (True):
    print("Single coil steps")
    myStepper.step(100, RaspiMotorHAT.FORWARD, RaspiMotorHAT.SINGLE)
    myStepper.step(100, RaspiMotorHAT.BACKWARD, RaspiMotorHAT.SINGLE)

    print("Double coil steps")
    myStepper.step(100, RaspiMotorHAT.FORWARD, RaspiMotorHAT.DOUBLE)
    myStepper.step(100, RaspiMotorHAT.BACKWARD, RaspiMotorHAT.DOUBLE)

    print("Interleaved coil steps")
    myStepper.step(100, RaspiMotorHAT.FORWARD, RaspiMotorHAT.INTERLEAVE)
    myStepper.step(100, RaspiMotorHAT.BACKWARD, RaspiMotorHAT.INTERLEAVE)

    print("Microsteps")
    myStepper.step(100, RaspiMotorHAT.FORWARD, RaspiMotorHAT.MICROSTEP)
    myStepper.step(100, RaspiMotorHAT.BACKWARD, RaspiMotorHAT.MICROSTEP)
