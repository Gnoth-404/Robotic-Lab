#!/usr/bin/env python3

import rospy # Python library for ROS
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np
scale = 1
delta = 0
ddepth = cv2.CV_16S

def process_image(frame):
  grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# Gradient-X
  grad_x = cv2.Sobel(grey,ddepth,1,0,ksize = 3, scale = scale, delta = delta,borderType = cv2.BORDER_DEFAULT)
# Gradient-Y
  grad_y = cv2.Sobel(grey,ddepth,0,1,ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
# converting back to uint8
  abs_grad_x = cv2.convertScaleAbs(grad_x) 
  abs_grad_y = cv2.convertScaleAbs(grad_y)
#	approximate the gradient
  sobel = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)
  return sobel

def callback(data):
 
  # Used to convert between ROS and OpenCV images
  br = CvBridge()
 
  # Output debugging information to the terminal
  rospy.loginfo("receiving video frame")
   
  # Convert ROS Image message to OpenCV image
  frame = br.imgmsg_to_cv2(data,"bgr8")
  frame = np.array(frame, dtype =np.uint8)
  display_process_image =process_image(frame)
  # Display image
  cv2.imshow("camera", display_process_image)
   
  cv2.waitKey(1)
      
def receive_message():
 
  # Tells rospy the name of the node.
  # Anonymous = True makes sure the node has a unique name. Random
  # numbers are added to the end of the name. 
  rospy.init_node('video_sub_py', anonymous=True)
   
  # Node is subscribing to the video_frames topic
  rospy.Subscriber('/usb_cam/image_raw', Image, callback)
 
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()
 
  # Close down the video stream when done
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  receive_message()
