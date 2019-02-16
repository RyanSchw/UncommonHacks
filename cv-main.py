import numpy as np
import cv2

video = cv2.VideoCapture("./resources/red_dot_1.MOV")

lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])

while(True):
    # Capture frame-by-frame
    ret, frame = video.read()
    smaller_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_red, upper_red)


    # Our operations on the frame come here
    # Display the resulting frame
    cv2.imshow('frame',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
video.release()
cv2.destroyAllWindows()