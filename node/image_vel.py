#! /usr/bin/env python3

from __future__ import print_function
import rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



def image_callback(img_data):
    try:
        cv_image = bridge.imgmsg_to_cv2(img_data, "bgr8")
        #cv2.imshow("Image", cv_image)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print(e)
    (rows,cols,channels) = cv_image.shape

    cv2.imshow("Image window", draw_ball(cv_image))
    cv2.waitKey(3)

def move_robot(position):
   error_num = 800/2-position
   
   #have one variable that holds the last position, and over write it every time
   #have an error case where if the position is whack, use the last error case
   move.angular.z = 0.005*error
   move.linear.x = 0.1

#was 0.2
#what i could also do is do like, while it is -1, do an extra sharp turn

def draw_ball(image):
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

   blur = cv2.GaussianBlur(gray, (5,5),0)

   ret, binary = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

   row_num = 750

   row = binary[row_num]
   
   
   i=0
   j=0
   flposition = []
   lookup = 0

   for element in row:
      i = 1+i
      if(element == lookup):
         j = j+1
         flposition.append(i)
         lookup = 255
         if(j==2):
            break

   if(np.size(flposition)==0):
      flposition.append(0)

   position = np.int(np.mean(flposition))
   #this above gives the position of the line, what i can do
   # is do classic pid from the error between the middle of the
   #screen and the position of the centre of the line

   move_robot(position)

   final_image = cv2.circle(image, (position,row_num), 20, (0,0,255), -1)

   return final_image
   


#This publishes the Twist data of the robot to ROS
#To check that this is working, use rostopic list and rostopic echo at /cmd_vel
rospy.init_node('topic_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)
move = Twist()
#move.linear.x = 0.2
#move.angular.z = 1.5

#This subscribes to the raw image files from the camera
images_ros = rospy.Subscriber('/rrbot/camera1/image_raw', Image, image_callback)

#Trying to convert from ROS Image sensor_msgs.msg to cv Image
bridge = CvBridge()

while not rospy.is_shutdown():
    pub.publish(move)
    rate.sleep()
