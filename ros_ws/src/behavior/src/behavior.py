#!/usr/bin/env python
import owyl
from owyl import blackboard
import rospy
import numpy as np
import time
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import Point
class Behavior:
    def __init__(self,bb):
        self.blackboard=bb
        self.main_tree=self.create_main_tree()
    def create_main_tree(self):
        '''
            creates the main tree for owyl behavior tree

            Args:
                self
                The tree looks like this:
                                                       root
                                                        |
                                                   owyl.repeatAlways
                                                        |
                                                   owyl.sequence
                                                        |  
                            --------------------------------------------------------
                            |                           |                          |                  		                                      
                    owyl.selector                 self.TurnToBall            self.WalkToBall()        
                                                                                                                                                       
                  -------------------------                                   
                  |                       |                          
        self.CheckIfBall() 	   self.walkBackwards  


            Returns:
                Creates a tree and returns
                owyl.visit method to visit next nodes in the tree.
        '''
        tree = owyl.repeatAlways(
				     owyl.sequence(
						owyl.selector(self.CheckIfBall(),self.walkBackwards ())
						,self.TurnToBall ()
						,self.WalkToBall ()
							
		)
	)
        return owyl.visit(tree,blackboard=self.blackboard)   
    def is_ball_centered(self,frame_range):
		return True if (self.blackboard['ball'].x>frame_range[0] and self.blackboard['ball'].x<frame_range[1]) else False
    def center_ball(self):
	    while not self.is_ball_centered([0.2,0.8]):
		    print self.blackboard['ball'].x,self.is_ball_centered([0.2,0.8])
		    if self.blackboard['ball'].x<0.5:
			    print 'left'
			    self.blackboard["robot_cmd_pub"].publish("TURN_LEFT")
			    #self.delay(3)
			    #rospy.Timer(rospy.Duration(3), self.timer_callback, oneshot=True)
			    #self.blackboard["robot_cmd_pub"].publish("STOP")
			    self.delay(1)
		    else:
			    print 'right'
			    
	 		    self.blackboard["robot_cmd_pub"].publish("TURN_RIGHT")
			    #self.delay(3)
			    #rospy.Timer(rospy.Duration(3), self.timer_callback, oneshot=True)
			    #self.blackboard["robot_cmd_pub"].publish("STOP")
			    self.delay(1)	
	
	    self.blackboard["robot_cmd_pub"].publish("STOP")
    def timer_callback(self,event):
	 self.blackboard["robot_cmd_pub"].publish("STOP")
    def delay(self,t_sec):      
        time.sleep(t_sec)    
    @owyl.taskmethod
    def CheckIfBall(self,**kwargs):
        # #rospy.loginfo("checking if ball exists")
	print "checking"
	count   = 0 
	self.delay(1)
        if not self.blackboard['ball_detected']:
		while count <50000:
				if self.blackboard["ball_detected"]:
					self.blackboard["ball_detected"] = False	
					yield True
				count +=1
				#print count
		yield False
	else:
		self.blackboard["ball_detected"] = False
		yield True

    @owyl.taskmethod
    def walkBackwards (self,**kwargs):
	  print 'walk back'
	  if not  self.blackboard['ball_detected']:
	    	self.blackboard["robot_cmd_pub"].publish("WALK_BCK")
		self.delay(2)
		self.blackboard["robot_cmd_pub"].publish("STOP")
		self.delay(1)
		count = 0
		self.delay(1)
		while count <50000:
			  if self.blackboard["ball_detected"] :
				self.blackboard["ball_detected"] = False
				yield True
			  count+=1	 
		yield False
	  else:
		self.blackboard["ball_detected"] = False
		yield True
    @owyl.taskmethod
    def TurnToBall  (self,**kwargs):
		    
		    if self.blackboard['ball'].x<0.3:
			    print 'left',2*(1-self.blackboard['ball'].x)
			    self.blackboard["robot_cmd_pub"].publish("TURN_LEFT")
			    #self.delay(3)
			    #rospy.Timer(rospy.Duration(3), self.timer_callback, oneshot=True)
			    #self.blackboard["robot_cmd_pub"].publish("STOP")
			    
			    self.delay(2*(1-self.blackboard['ball'].x))
			    self.blackboard["robot_cmd_pub"].publish("STOP")
			    self.delay(1)
			    board["ball_centered"] = True
		    elif self.blackboard['ball'].x>0.7:
			    print 'right',2*self.blackboard['ball'].x
			    
	 		    self.blackboard["robot_cmd_pub"].publish("TURN_RIGHT")
			    #self.delay(3)
			    #rospy.Timer(rospy.Duration(3), self.timer_callback, oneshot=True)
			    #self.blackboard["robot_cmd_pub"].publish("STOP")
			    self.delay(self.blackboard['ball'].x)
				    
			    self.blackboard["robot_cmd_pub"].publish("STOP")
			    self.delay(1)
			    board["ball_centered"] = True
		    print self.blackboard['ball'].x,"without turning"
		    yield True		    
#	    print 'turning',self.blackboard['ball_detected']
#	    print self.blackboard['ball'].x,self.is_ball_centered([0.2,0.8])
#	    while not self.is_ball_centered([0.2,0.8]):
#		    #self.blackboard['ball_detected'] = False
#		    if self.blackboard['ball'].x<0.5:
#			    print 'left'
#			    self.blackboard["robot_cmd_pub"].publish("TURN_LEFT")
#			    #self.delay(3)
#			    #rospy.Timer(rospy.Duration(3), self.timer_callback, oneshot=True)
#			    #self.blackboard["robot_cmd_pub"].publish("STOP")
#			    self.delay(1)
#			    board["ball_centered"] = True
#		    else:
#			    print 'right'
#			    
#	 		    self.blackboard["robot_cmd_pub"].publish("TURN_RIGHT")
#			    #self.delay(3)
#			    #rospy.Timer(rospy.Duration(3), self.timer_callback, oneshot=True)
#			    #self.blackboard["robot_cmd_pub"].publish("STOP")
#			    self.delay(1)
#			    board["ball_centered"] = True
#	    self.blackboard["robot_cmd_pub"].publish("STOP")
#	    self.delay(1)			
##	    if board["ball_centered"] :
##			board["ball_centered"] =False
##			yield True
##	    else:
##			yield False    
	    #yield True
    @owyl.taskmethod
    def WalkToBall(self,**kwargs)  :
	  print'walk to balllllllllllllllllllllllllllllllllll'
	  #self.center_ball()
#	  while (self.is_ball_centered([0.2,0.8]) ): 
#	  		self.blackboard["robot_cmd_pub"].publish('WALK_FWD' )
	  #self.delay(2)
	  self.blackboard["robot_cmd_pub"].publish('WALK_FWD' )
	  self.delay(4)
	  self.blackboard["robot_cmd_pub"].publish("STOP")
	  self.delay(1)
	  yield True
    def stop_movement():
        '''
               A publihser function to the robot.  It will stop any command send to the robot.   
              publishes to /act/robot/send_move_command
        '''
        if not rospy.is_shutdown():
            self.blackboard["robot_cmd_pub"].publish('STOP' )

def BallDetected  (data):	
	
	board["ball_centered"]  = False
	board["ball_detected"]  = True
	board['ball'] = data
	#print "here"

if __name__=="__main__":
    # Initialize Node
    rospy.init_node('behavior', anonymous = False)
    robot_cmd_pub = rospy.Publisher('/command', String, queue_size = 1)
    # Initialize subscriber
    rospy.Subscriber('/ball_pose',Point,BallDetected)
    # create an object of black board 
    board=blackboard.Blackboard("My board")
    # publishers on board
    board["robot_cmd_pub"]  = robot_cmd_pub
    board['ball'] = Point(0,0,0)
    # Init variables
    board["ball_detected"] = True
    board["ball_centered"] = True
    # Create a behavior tree using the blackboard object board
    be=Behavior(board)
    be_tree=be.main_tree 
    # Wait for bluetooth to connect
    rate=rospy.Rate(100)#100hz
    # rospy.spin()
    while not rospy.is_shutdown():
        ##rospy.loginfo("Here in the loop")
        be_tree.next()
        rate.sleep()


