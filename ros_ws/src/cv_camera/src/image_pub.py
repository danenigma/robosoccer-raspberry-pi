#!/usr/bin/env python
__Author__ = 'daniel'
import rospy
import cv2
import numpy as np
from geometry_msgs.msg import Point
from picamera.array import PiRGBArray
from picamera import PiCamera
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
class ImagePublisher:
    NODE_NAME = 'image_publisher'
    def __init__(self):
	self.publisher = rospy.Publisher('/camera',Image, queue_size=1)
        self.bridge = CvBridge()
        self.camera = PiCamera()
	self.camera.resolution = (320, 240)
	self.camera.framerate = 90
	self.rawCapture = PiRGBArray(self.camera, size=(320, 240))
    def run(self):
	rospy.init_node(self.NODE_NAME, anonymous=False)
	# capture frames from the camera
	for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array
		if image is not None:
			ros_image  = self.bridge.cv2_to_imgmsg(image,"bgr8")
			self.publisher.publish(ros_image)
			cv2.imshow('pub',image)
		key = cv2.waitKey(1) & 0xFF
		self.rawCapture.truncate(0)	
if __name__ == '__main__':
    rospy.loginfo("Starting " + ImagePublisher.NODE_NAME)
    image_pub = ImagePublisher()

    try:
       image_pub.run()
    except KeyboardInterrupt:
        rospy.loginfo("Stopping " + image_pub.NODE_NAME)
    



