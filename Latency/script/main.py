#!/usr/bin/env python3

import NmeaPublisher 
import rospy
import checkmessage


def main():
    rospy.init_node('NmeaPublisher')
    sender = NmeaPublisher()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        checkmessage.check()
        rate.sleep()

if __name__ == '__main__':
    
    main()