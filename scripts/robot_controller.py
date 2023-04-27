#!/usr/bin/env python

from __future__ import print_function

import rospy
from cr_week6_test.srv import *
from cr_week6_test.msg import perceived_info, robot_info

def callback(data):    
    pub = rospy.Publisher('robot_info', robot_info, queue_size=10)

    try:
        # try to connect to service 
        compute = rospy.ServiceProxy('robot_prediction', predict_robot_expression)

        # compute predictions using data obtained from the subscriber
        response = compute(data)

        # construct a message
        r_info = robot_info()
        r_info.id = data.id
        r_info.p_happy = response.p_happy
        r_info.p_sad= response.p_sad
        r_info.p_neutral = response.p_neutral

        # publish robot info values
        pub.publish(r_info)

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


def listener():
    # Initialise node
    rospy.init_node('robot_expression', anonymous=True)

    # wait for service
    rospy.wait_for_service('robot_prediction')

    # subscribe to perceived_info and send data to callback
    rospy.Subscriber('perceived_info', perceived_info, callback, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    listener()
