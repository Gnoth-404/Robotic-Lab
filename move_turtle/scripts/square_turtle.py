#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from math import radians

import sys

def move():
    rospy.init_node('turtlesim', anonymous=True)
    pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)

    rate = rospy.Rate(10)
    turn_cmd = Twist()
    turn_cmd.linear.x = 0
    turn_cmd.angular.z = radians(45); #45 deg/s in radians/s
    r = rospy.Rate(5);
    count = 0  
    move_cmd = Twist()
    move_cmd.linear.x = 0.1
    while not rospy.is_shutdown():
        rospy.loginfo("Going Straight")
        for x in range(0,10):
            pub.publish(move_cmd)
            r.sleep()
	    # turn 90 degrees
        rospy.loginfo("Turning")
        for x in range(0,10):
            pub.publish(turn_cmd)
            r.sleep()            
        count = count + 1
        if(count == 4): 
            count = 0
        if(count == 0): 
            rospy.loginfo("TurtleBot should be close to the original starting position (but it's probably way off)")
 
if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass
