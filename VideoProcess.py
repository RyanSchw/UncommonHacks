import numpy as np
import cv2
import time
import pickle
import imutils

from Vec2d import Vec2d
from Sample import Sample
from vis import SampleVisualizer


# Process a video and creates array of tracked points and velocity
class VideoProcess():
    def __init__(self, video_path="./resources/red_dot_1_down.avi", debug=False):
        self.debug = debug
        self.video_path = video_path
        self.scale_factor = 1

        self.low_mask = np.array([0, 140, 40])  # Mask for color detection
        self.up_mask = np.array([255, 255, 250])
        self.path = []  # Final output path for model
        self.last_frame = None

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
        vizer.plot_track(max_vel=self.max_vel * 0.8)

    def color_detect(self, frame):
        # Convert RGB to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Mask out non-red pixels
        mask = cv2.inRange(hsv, self.low_mask, self.up_mask)

        if self.debug:
            cv2.imshow('frame', frame)
            cv2.waitKey(2)

        # Find location of pixels
        return self.find_ball_location(mask)
    
    def motion_detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if self.last_frame is None:
            self.last_frame = gray
            return -1
        frameDelta = cv2.absdiff(self.last_frame, gray)

        thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)


        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        largest_area = -1
        sel_cont = None
        # loop over the contours
        for c in cnts:
            area = cv2.contourArea(c)
            if area > largest_area:
                sel_cont = c
                largest_area = area

        (x, y, w, h) = cv2.boundingRect(sel_cont)
        
        if self.debug:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('frame', frame)
            cv2.waitKey(2)

        self.last_frame = gray
        return Vec2d(x + w/2, y + h/2)

    def calculate_velocity(self, current_time, last_time, current_pos, last_pos):
        cur_vel = Vec2d(0, 0)
        delta_time = (current_time - last_time)  # Calculate dT in seconds

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

        width = video.get(cv2.CAP_PROP_FRAME_WIDTH) * self.scale_factor
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT) * self.scale_factor

        scale_vector = Vec2d(width, height)

        last_time = -1
        last_pos = Vec2d(-1, -1)

        max_frames = 800
        frame_index = 0

        while(video.isOpened() and frame_index < max_frames):
            frame_index += 1
            ret, frame = video.read()

            # Process frame if it is available
            if(ret):
                # Process frame to grab locations
                # Downsize frame
                frame = cv2.resize(
                    frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)

                # cur_pos = self.color_detect(frame)
                cur_pos = self.motion_detect(frame)

                if cur_pos != -1 and cur_pos != Vec2d(0,0):
                    # Scale down vector to a 0.0 -> 1.0 scale
                    cur_pos = cur_pos.elm_div(scale_vector)

                    # Calculate frame velocity
                    cur_time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                    cur_vel = self.calculate_velocity(
                        cur_time, last_time, cur_pos, last_pos)

                    if cur_vel.mag() < 300:
                        sample = Sample(cur_pos, cur_vel, Vec2d(0, 0), cur_time)
                        self.path.append(sample)

                    last_time = cur_time
                    last_pos = cur_pos

            else:
                print("Processing complete " + str(len(self.path)))
                # print(path)
                break

        # When everything done, release the capture
        video.release()
        if self.debug:
            cv2.destroyAllWindows()

        return self.path


if __name__ == "__main__":
    start_time = time.time()
    p = VideoProcess(
        video_path="./resources/car_test_2_motion.webm", debug=False)
    p.process_video()

    # p.view_path()

    print(Sample.serialize_array(p.path))

    print(time.time() - start_time)
