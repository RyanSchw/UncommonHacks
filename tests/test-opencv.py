# Ensures that correct version of open cv is working
import cv2

assert cv2.__version__ == "4.0.0"

print("OpenCV is working properly")