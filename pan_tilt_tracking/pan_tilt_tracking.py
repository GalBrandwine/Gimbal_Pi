# USAGE
# python pan_tilt_tracking.py --cascade haarcascade_frontalface_default.xml

import argparse
import signal
import sys
import time
# import necessary packages
from multiprocessing import Manager
from multiprocessing import Process

import cv2
from imutils.video import VideoStream
from pan_tilt import pan_tilt as PanTilt
from pid_controller.objcenter import ObjCenter
from pid_controller.pid import PID

# define the range for the motors
servoRange = (-90, 90)


# function to handle keyboard interrupt
def signal_handler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # disable the servos
    PanTilt.servo_enable(1, False)
    PanTilt.servo_enable(2, False)

    # exit
    sys.exit()


def obj_center(args, objX, objY, centerX, centerY):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # start the video stream and wait for the camera to warm up
    vs = VideoStream(usePiCamera=False).start()
    time.sleep(2.0)

    # initialize the object center finder
    # obj = ObjCenter(args["cascade"])
    obj = ObjCenter("/home/pi/Gimbal_Pi/pan_tilt_tracking/haar.xml")

    img = vs.read()
    scale_percent = 30  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # loop indefinitely
    while True:
        # grab the frame from the threaded video stream and flip it
        # vertically (since our camera was upside down)
        frame = vs.read()
        # frame = cv2.flip(frame, 0)

        # Resize image
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        
        # Overcome mirror effect
        frame = cv2.flip(frame, 1)

        # calculate the center of the frame as this is where we will
        # try to keep the object
        (H, W) = frame.shape[:2]
        centerX.value = W // 2
        centerY.value = H // 2
        cv2.circle(frame,(centerX.value,centerY.value), 5, (0,0,255), -1)
        
        # find the object's location
        objectLoc = obj.update(frame, (centerX.value, centerY.value))
        ((objX.value, objY.value), rect) = objectLoc
        cv2.circle(frame,(objX.value, objY.value), 5, (0,255,0), -1)

        # extract the bounding box and draw it
        if rect is not None:
            (x, y, w, h) = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
                          2)
            #cv2.circle(frame,(int((x + w)//2), int((y + h)//2)), 10, (0,255,255), 1)

        # display the frame to the screen
        cv2.imshow("Pan-Tilt Face Tracking", frame)
        cv2.waitKey(1)


def pid_process(output, p, i, d, objCoord, centerCoord):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # create a PID and initialize it
    p = PID(p.value, i.value, d.value)
    p.initialize()

    # loop indefinitely
    while True:
        # calculate the error
        error = centerCoord.value - objCoord.value
        print(centerCoord.value,objCoord.value,error)
        # update the value
        output.value = p.update(error)


def in_range(val, start, end):
    # determine the input vale is in the supplied range
    return (val >= start and val <= end)


def go(pan, tlt):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # Init
    #PanTilt.tilt(90)
    #PanTilt.pan(90)
    #time.sleep(1)
    
    # loop indefinitely
    while True:
        # the pan and tilt angles are reversed
        panAngle = 1 * pan.value
        tltAngle = 1 * tlt.value

        # if the pan angle is within the range, pan
        if in_range(panAngle, servoRange[0], servoRange[1]):
            PanTilt.pan(panAngle)

        # if the tilt angle is within the range, tilt
        if in_range(tltAngle, servoRange[0], servoRange[1]):
            PanTilt.tilt(tltAngle)


# check to see if this is the main body of execution
if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", type=str, required=False,
                    help="path to input Haar cascade for face detection")
    args = vars(ap.parse_args())
    print("srarted")
    # start a manager for managing process-safe variables
    with Manager() as manager:
        # enable the servos
        PanTilt.servo_enable(1, True)
        PanTilt.servo_enable(2, True)

        # set integer values for the object center (x, y)-coordinates
        centerX = manager.Value("i", 0)
        centerY = manager.Value("i", 0)

        # set integer values for the object's (x, y)-coordinates
        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)

        # pan and tilt values will be managed by independed PIDs
        pan = manager.Value("i", 0)
        tlt = manager.Value("i", 0)

        # set PID values for panning
        panP = manager.Value("f", 0.09)
        panI = manager.Value("f", 0.08)
        panD = manager.Value("f", 0.002)

        # set PID values for tilting
        tiltP = manager.Value("f", 0.11)
        tiltI = manager.Value("f", 0.10)
        tiltD = manager.Value("f", 0.002)

        # we have 4 independent processes
        # 1. objectCenter  - finds/localizes the object
        # 2. panning       - PID control loop determines panning angle
        # 3. tilting       - PID control loop determines tilting angle
        # 4. setServos     - drives the servos to proper angles based
        #                    on PID feedback to keep object in center
        processObjectCenter = Process(target=obj_center,
                                      args=(args, objX, objY, centerX, centerY))
        processPanning = Process(target=pid_process,
                                 args=(pan, panP, panI, panD, objX, centerX))
        processTilting = Process(target=pid_process,
                                 args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
        processSetServos = Process(target=go, args=(pan, tlt))

        # start all 4 processes
        processObjectCenter.start()
        processPanning.start()
        processTilting.start()
        processSetServos.start()

        # join all 4 processes
        processObjectCenter.join()
        processPanning.join()
        processTilting.join()
        processSetServos.join()

        # disable the servos
        PanTilt.servo_enable(1, False)
        PanTilt.servo_enable(2, False)
