from djitellopy import tello
import KeyPressModule as kp
from time import sleep, time
import cv2
import numpy as np
import math

# ----- PARAMETERS --------
# tello in terms of speed is not repeatable
# upon testing it went 117 cm in 10 seconds
fspeed = 150 / 10  # forward speed in cm/s (it says 15cm/s)
aspeed = 360 / 10  # 10 seconds to rotate 360 degrees/2 (used 50d/s)
interval = 0.25

# In the example we took the interval as 1seconds.. but its too long
# so reduce is to 0.25
# based on this info we have the speed and interval
# every unit of our map will represent a certain amount of distance
# and a certain amount of angle

dInterval = fspeed * interval
aInterval = aspeed * interval
# this will give us the distance and the angle we move every unit
x, y = 500, 500
# distance angle well check what is happening
a = 0
yaw = 0

kp.init()
# drone = tello.Tello()
# drone.connect()
# print(drone.get_battery())

points = []

# have to find the value of how far we have travelled
# lets call them x,y
# whenever we press a key.. x and y values should change
# at every button pressed, we need to add to distance and angle
# at every key press, we have to update angle and distance

# angle wont reset since the drone will maintain that angle and itll
# continue to add on
# distance will be reset after every key press

# when travelling, we travel with dInterval
# but when not going forward, we need to change our angle

# in yaw rotation, well check our previous angle and add to it

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    d = 0
    global x, y, yaw, a

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = aspeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = -aspeed
        yaw += aInterval

    if kp.getKey("q"):
        # drone.land()
        sleep(3)

    #if kp.getKey("e"):
        #drone.takeoff()

    if kp.getKey("z"):
        cv2.imwrite(
            f"/Users/arnavpuri/Documents/drone/images/{time.time()}.jpg")

    # we have updated our values, now need to convert to cartesian plane
    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, (point[0], point[1]), 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (points[-1][0], points[-1][1]), 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500)/ 100}, '
                     f'{(points[-1][1] - 500)/ 100}m)',
                (points[-1][0] + 10, points[-1][1] + 10),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)


# need to check if the button is pressed.
# if it pressed, change rc control values
while True:
    vals = getKeyboardInput()
    # drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    points.append([vals[4], vals[5]])
    # uint8 -> 0 - 255

    drawPoints(img, points)
    cv2.imshow("OUTPUT", img)
    cv2.waitKey(1)
