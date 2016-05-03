#!/usr/bin/env python
from ball_tracker import *
goal = BallTracker()
try:
	goal.run()
except KeyboardInterrupt:
	rospy.loginfo("Stopping " + goal.NODE_NAME)

