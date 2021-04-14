import cv2
import numpy as np
from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
print("drone battery: {}".format(drone.get_battery()))

#cap = cv2.VideoCapture(0)
drone.streamon()

drone.takeoff()
drone.send_rc_control(0, 0, 25, 0)
sleep(2.2)

w, h = 360, 240
fbRange = [6200, 6800]
# proportional, integral, derivative
pid = [0.4, 0.4, 0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier(
        "/Users/arnavpuri/Documents/drone_programming/resources/haarcascade_frontalface_default.xml")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(img_gray, 1.2, 8)

    # create a list of all these faces and then the area of all these
    # faces
    # there will be multiple faces. find the biggest one and track that
    # first list will have info of centre point
    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # get the center of the face
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(drone, info, w, pid, pError):

    area = info[1]
    x, y = info[0]
    fb = 0
    # find the error by finding how off is x from center of the rectangle
    # find out how far away is our object from the center
    # x is the object
    error = x - w//2

    # use equation of pid
    # pid is a constant value
    # changing the sensitivity of the error by pid[0]
    speed = pid[0] * error + pid[1] * (error - pError)

    #clip the speed -> -100 to 100
    speed = int(np.clip(speed, -100, 100))


    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[2]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    # define here if x is in center for speed
    if x == 0:
        speed = 0
        error = 0

    drone.send_rc_control(0, fb, 0, speed)

    return error


while True:
    #_, img = cap.read()
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(drone, info, w, pid, pError)
    # the center value will be used to rotate and the area value will be
    # used to go forwards and backwards
    print("center: {}, area: {}".format(info[0], info[1]))
    cv2.imshow("output", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        drone.land()
        break
