# Gimbal_Pi
A gimbal module for raspberry pi.

A few years ago iv'e made a cute [openCV-face-tracking-robot](https://youtu.be/GF0xc0aUvpI), although this robot worked,
it worked slow and it lose track of my face if I move'd quickly.

The problem was it has no PID controller, for smoothing and adjusting Errors 
(distance between face-rectangle center, to frame center).
This project aims to optimize face tracking with a PID controller.

## Dedicated for this Raspberry_pi_HAT:
* You can by it from [here](https://www.aliexpress.com/item/DIY-Your-Robot-U-Geek-Stepper-Motor-HAT-for-Raspberry-Pi-Model-A-B-or-Pi/32536369104.html?spm=2114.search0104.3.37.66d42fb4nV1voe&ws_ab_test=searchweb0_0,searchweb201602_5_10065_10068_319_10059_10884_317_10887_10696_321_322_10084_453_10083_454_10103_10618_10307_537_536,searchweb201603_54,ppcSwitch_0&algo_expid=b600b4f1-d521-48bd-9996-7c9b15d6836e-5&algo_pvid=b600b4f1-d521-48bd-9996-7c9b15d6836e&transAbTest=ae803_5)

![picture alt](https://ae01.alicdn.com/kf/HTB1HN_xa5rxK1RkHFCcq6AQCVXaY/DIY-Robot-UGEEK-Stepper-Motor-HAT-for-Raspberry-Pi-3-Model-B-3B-3A-2B-Zero.jpg)
![picture alt](https://ae01.alicdn.com/kf/HTB1jgvBa5nrK1Rjy1Xcq6yeDVXae/DIY-Robot-UGEEK-Stepper-Motor-HAT-for-Raspberry-Pi-3-Model-B-3B-3A-2B-Zero.jpg)

* This Hat module will contain relevant libraries for operating this breakout.

# Mainly concentrated on PWM servo driver.
# Also, there will be a PID controller, and en example for using it.

## Getting started:
1. Need to raspi-config inorder to activate i2c support!

