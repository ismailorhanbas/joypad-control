#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy

import pygame

def scale_data(value, axis):
    # Scale a value in the range [-1.0, 1.0] to the range [255, 0]
    if axis == 1:  # Vertical axis
        return int((1.0 - value ) * 127.5)
    else:  # Horizontal axis
        return int((1.0 - value) * 127.5)

def joystick_publisher():
    # Initialize Pygame
    pygame.init()
    pygame.joystick.init()

    # Set up joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Initialize ROS node and publisher
    rospy.init_node('joystick_publisher')
    pub = rospy.Publisher('joy', Joy, queue_size=10)
    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        # Get joystick data
        pygame.event.get()
        axes = [scale_data(joystick.get_axis(i), i) for i in range(joystick.get_numaxes())]
        buttons = [int(scale_data(joystick.get_button(i), 2)) for i in range(joystick.get_numbuttons())]

        # Create Joy message
        joy_msg = Joy()
        joy_msg.header.stamp = rospy.Time.now()
        joy_msg.axes = axes
        joy_msg.buttons = buttons

        # Publish Joy message
        pub.publish(joy_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        joystick_publisher()
    except rospy.ROSInterruptException:
        pass
