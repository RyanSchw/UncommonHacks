import numpy as np
import cv2
import time
from utils import Vec2d, Sample
from vis import SampleVisualizer

DEBUG = False

video = cv2.VideoCapture("./resources/red_dot_1_down.avi")

# ####### Maybe use thsis code for down sampling the video to 10 fps...
# # Process down video to get target FPS
# video_fps = round(video.get(cv2.CAP_PROP_FPS))
# frame_skip = video_fps / 10
# # Estimate total number of frames in video
# est_total_frames = video_fps * 20
# # Generate array of frame indices to include
# desired_frames = frame_skip * np.arange(est_total_frames) 
# ########

# Mask for color detection
lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])

# Assuming that there is one major blob on the image, find
# the centroid of the blob and display it on the image
def find_ball_location(mask):
    M = cv2.moments(mask)

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return Vec2d(cX, cY)


path = []
last_frame_timestamp = -1
last_pos = Vec2d(-1, -1)
while(video.isOpened()):

    # Measure frame reading speeds
    start_time = time.time()
    ret, frame = video.read()
    frame_time = time.time()

    # Process frame if it is available
    if(ret):

        # Process frame to grab locations
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    # Downsize frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        # Convert RGB to HSV
        mask = cv2.inRange(hsv, lower_red, upper_red)       # Mask out non-red pixels
        cur_pos = find_ball_location(mask)                 # Find location of pixels

        # Calculate frame velocity
        frame_timestamp = video.get(cv2.CAP_PROP_POS_MSEC)
        cur_vel = Vec2d(0,0)
        delta_time = (frame_timestamp - last_frame_timestamp) / 1000
        if last_frame_timestamp > 0 and delta_time > 0:
            
            # Calculate displacment
            displacment = cur_pos - last_pos
            # Calculate velocity
            cur_vel = displacment / delta_time
            print(cur_vel)

        last_pos = cur_pos
        last_frame_timestamp = frame_timestamp


        sample = Sample(cur_pos, cur_vel, Vec2d(0,0), frame_timestamp)
        path.append(sample)



        # Debug print statements
        if DEBUG:
            process_time = time.time()
            print("Frame: %.5f " % (frame_time - start_time) + " Process: %.5f" % (process_time - frame_time))
            cv2.imshow('frame', mask)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print("Processing complete " + str(len(path)))
        # print(path)
        break

# When everything done, release the capture
video.release()
cv2.destroyAllWindows()

vizer = SampleVisualizer(path)
vizer.plot_meas("pos")