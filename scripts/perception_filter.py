#!/usr/bin/env python

from __future__ import print_function

import rospy
import random
from cr_week6_test.msg import object_info, human_info, perceived_info


class listener:
    def __init__(self):
        # Initialise node
        rospy.init_node('perception_filter', anonymous=True)

        # subscribe to object_info and send data to callback_1
        rospy.Subscriber('object_info', object_info, self.callback_1, queue_size=10)

        # subscribe to human_i,nfo and send data to callback_2
        rospy.Subscriber('human_info', human_info, self.callback_2, queue_size=10)

        # spin() simply keeps python from exiting until the node is stopped
        rospy.spin() 
        
    def callback_1(self, data):    
        #initialiase variables
        self.O = data.object_size

    def callback_2(self, data):    
        pub = rospy.Publisher('perceived_info', perceived_info, queue_size=10)

        obj = object_info()
        hum = human_info()

        #initialiase variables
        HA = data.human_action
        HE = data.human_expression

        # Get random integer value
        random_int = random.randint(1,8)

        if random_int == 1:
            self.O = 0
        elif random_int == 2:
            HA = 0
        elif random_int == 3:
            HE = 0
        elif random_int == 4:
            self.O = 0
            HA = 0
        elif random_int == 5:
            self.O = 0
            HE = 0
        elif random_int == 6:
            HA = 0
            HE = 0
        elif random_int == 7:
            self.O = 0
            HA = 0
            HE = 0
        elif random_int == 8:
            self.O = obj.object_size
            HA = hum.human_action
            HE = hum.human_expression
        
        # PUblish perceived info message
        p_i = perceived_info()

        p_i.id = data.id
        p_i.object_size = self.O
        p_i.human_action = HA
        p_i.human_expression = HE

        #rospy.loginfo(p_i)

        pub.publish(p_i)

if __name__ == '__main__':
    lis = listener()