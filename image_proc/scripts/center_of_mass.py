#!/usr/bin/env python3

import rospy # Python library for ROS
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np

def process_image(frame):
# Convert to grey image
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.float32)/25
    img_filter=cv2.filter2D(grey,-1, kernel)
    ret,thresh = cv2.threshold(img_filter, 30, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh,
    cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    maxArea = -1
    for cnt in contours:
    	if cv2.contourArea(cnt) > maxArea:
            maxArea = cv2.contourArea(cnt)
            out = cnt
    cv2.drawContours(frame, out, -1, (0,255,0), 3)
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
    cv2.putText(frame, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)
    return frame
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
