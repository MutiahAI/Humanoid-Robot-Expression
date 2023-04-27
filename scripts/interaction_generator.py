#!/usr/bin/env python

import rospy
import random
from cr_week6_test.msg import object_info, human_info

def talker():
    # Initialise Publisher
    pub_1 = rospy.Publisher('object_info', object_info, queue_size=10)
    pub_2 = rospy.Publisher('human_info', human_info, queue_size=10)

    # Initialise node
    rospy.init_node('int_generator', anonymous=True)
    # Set rate
    rate = rospy.Rate(0.1) # Every 10 seconds
    # Counting ID
    id_count = 0

    obj = object_info()
    human = human_info()

    while not rospy.is_shutdown():
        # ID increament per generation
        id_count += 1

        #object_info.id = id_count
        obj.id = id_count
        human.id = id_count

        #print(id_count)
        obj.object_size = random.randint(1,2)
        human.human_action = random.randint(1,3)
        human.human_expression = random.randint(1,3)

        # Useful during testing to display and log values
        #rospy.loginfo(obj)
        #rospy.loginfo(human)

        # Publish values
        pub_1.publish(obj)
        pub_2.publish(human)

        rate.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass