import numpy as np
import cv2
import time
from utils import Vec2d, Sample
from vis import SampleVisualizer


# Process a video and creates array of tracked points and velocity
class VideoProcess():
    def __init__(self, video_path="./resources/red_dot_1_down.avi", debug=False):
        self.debug = debug
        self.video_path = video_path

        self.low_mask = np.array([0,140,40]) # Mask for color detection
        self.up_mask = np.array([255,255,240])
        self.path = []  # Final output path for model

        # Keep track of maximum velocity when processing
        self.max_vel = 0

    # Assuming that there is one major blob on the image, find
    # the centroid of the blob and display it on the image
    def find_ball_location(self, mask):
        M = cv2.moments(mask)

        if M["m00"] == 0:
            return -1

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        return Vec2d(cX, cY)

    def view_path(self):
        vizer = SampleVisualizer(self.path)
        vizer.plot_track(max_vel=250)

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        # Convert RGB to HSV
        mask = cv2.inRange(hsv, self.low_mask, self.up_mask)       # Mask out non-red pixels

        if self.debug:
            cv2.imshow('frame', mask)
            cv2.waitKey(1)

        return self.find_ball_location(mask)                 # Find location of pixels

    def calculate_velocity(self, current_time, last_time, current_pos, last_pos):
        cur_vel = Vec2d(0,0)
        delta_time = (current_time - last_time) / 1000   # Calculate dT in seconds

        if last_time > 0 and delta_time > 0:
            # Calculate displacment
            displacment = current_pos - last_pos
            # Calculate velocity
            cur_vel = displacment / delta_time
            cur_vel_mag = cur_vel.mag()
            if cur_vel_mag > self.max_vel:
                self.max_vel = cur_vel_mag
        return cur_vel

    def process_video(self):
        video = cv2.VideoCapture(self.video_path)
        
        last_time = -1
        last_pos = Vec2d(-1, -1)

        max_frames = 1000
        frame_index = 0
        while(video.isOpened() and frame_index < max_frames):
            frame_index += 1
            ret, frame = video.read()

            # Process frame if it is available
            if(ret):
                # Process frame to grab locations
                frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)    # Downsize frame
                cur_pos = self.process_frame(frame)

                if cur_pos == -1:
                    break
                
                # Calculate frame velocity
                cur_time = video.get(cv2.CAP_PROP_POS_MSEC)
                cur_vel = self.calculate_velocity(cur_time, last_time, cur_pos, last_pos)

                sample = Sample(cur_pos, cur_vel, Vec2d(0,0), cur_time)
                self.path.append(sample)

                last_time = cur_time
                last_pos = cur_pos
                
            else:
                print("Processing complete " + str(len(path)))
                # print(path)
                break

        # When everything done, release the capture
        video.release()
        if self.debug:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    p = VideoProcess(video_path="./resources/car_test_1.mp4", debug=True)
    p.process_video()
    p.view_path()