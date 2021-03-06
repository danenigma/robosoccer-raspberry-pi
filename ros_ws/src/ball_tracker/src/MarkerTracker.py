#!/usr/bin/env python
__Author__ = 'daniel'
import rospy
import cv2
import numpy as np
from geometry_msgs.msg import Point
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
class BallTracker:
    NODE_NAME = 'ball_tracker'

    def __init__(self):
        self.hsv_upper  = np.array([117, 255, 255], np.uint8)
        self.hsv_lower = np.array([79, 57, 14], np.uint8)
	self.publisher = rospy.Publisher('/ball_pose', Point, queue_size=10)
        #self.bridge = CvBridge()
        #self.image_subscriber = rospy.Subscriber("/cv_camera/image_raw", Image, self.callback)
	self.camera = PiCamera()
	self.camera.resolution = (426, 320)
	self.camera.framerate = 90
	self.camera.brightness = 80
	self.rawCapture = PiRGBArray(self.camera, size=(426, 320))
    def run(self):
	rospy.init_node(self.NODE_NAME, anonymous=False)
	# allow the camera to warmup
	#time.sleep(0.1)
	rate  = rospy.Rate(2)
	# capture frames from the camera
	for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array
		ball_pos  = self.detect_ball(image)
		
		if ball_pos is not None:
			self.publisher.publish(ball_pos)
			#rate.sleep()
		#print ball_pos
	        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# show the frame
		cv2.imshow("Frame", image)
		key = cv2.waitKey(10) & 0xFF
		self.rawCapture.truncate(0)	
		
    def detect_ball(self, frame):
        buffer_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # Gaussian Blur
        buffer_frame = cv2.cvtColor(buffer_frame, cv2.COLOR_BGR2HSV)  # Convert to HSV
        buffer_frame = cv2.inRange(buffer_frame, self.hsv_lower, self.hsv_upper)  # Check if each pixel is in boundary
        buffer_frame = cv2.dilate(buffer_frame, np.ones((20, 20), "uint8"))  # Dilate
        contours, hierarchy = cv2.findContours(buffer_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ball_contour = self.largest_contour(contours)
        if ball_contour != None:
            # Filter out smaller contours
	    #cv2.contourArea(ball_contour)
            if cv2.contourArea(ball_contour) > 300:	
	        if ball_contour != None:
	                (x,y),radius   = cv2.minEnclosingCircle(ball_contour)
			center  =(int(x),int(y))
			radius  = int(radius)
			cv2.circle(frame,center,radius,(255,0,0),2)
			height, width, channels = frame.shape
	                return Point(float(ball_contour[0][0][0]) / width, float(ball_contour[0][0][1]) / height, 0)
    def largest_contour(self, contours):
        max_contour = [0, None]  # [Area, Index]
        if contours:
            for idx, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > max_contour[0]:
                    max_contour = [area, contour]
            return max_contour[1]
    def set_hsv_range(self,lhsv,uhsv):
	self.hsv_lower = lhsv
	self.hsv_upper = uhsv



if __name__ == '__main__':
    rospy.loginfo("Starting " + BallTracker.NODE_NAME)
    ball = BallTracker()

    try:
       ball.run()
    except KeyboardInterrupt:
        rospy.loginfo("Stopping " + BallTracker.NODE_NAME)
    cv2.destroyAllWindows()



