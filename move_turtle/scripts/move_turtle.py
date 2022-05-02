#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
def move():
    rospy.init_node('turtlesim', anonymous=True)
    pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel = Twist()
    while not rospy.is_shutdown():
        vel.linear.x = 0.5
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0.5
        vel.angular.y = 0
        vel.angular.z = 1
        rospy.loginfo("Velocity: 0.5m/s; angular velocity: 0.5 rad/s")
        pub.publish(vel)
        rate.sleep()
 
 
if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass
