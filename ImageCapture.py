from djitellopy import tello
import cv2

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

#this stream will give us frames one by one and we can process them
drone.streamon()

#since it is a continuous number of frames, need to use a while loop
while True:
    #this will give us the individual image coming from the tello drone
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("IMAGE",img)
    cv2.waitKey(1)


