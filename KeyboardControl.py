from djitellopy import tello
import KeyPressModule as kp
from time import sleep, time
import cv2

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed
    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed
    if kp.getKey("a"):
        yv = speed
    elif kp.getKey("d"):
        yv = -speed

    if kp.getKey("q"):
        drone.land()
    if kp.getKey("e"):
        drone.takeoff()

    if kp.getKey("z"):
        cv2.imwrite(f"/Users/arnavpuri/Documents/drone/images/{time.time()}.jpg")


    return [lr, fb, ud, yv]


# need to check if the button is pressed.
# if it pressed, change rc control values
while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
