#!/usr/bin/env python

import math
from math import sin, cos, pi
import numpy as np
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

def covariance():
    pose_covariance_matrix = np.zeros((6,6))
    twist_covariance_matrix = np.ravel(np.zeros((6,6)))

    pose_covariance_matrix[[0,1,2,3,4,5], [0,1,2,3,4,5]] = [1/(10**5), 1/(10**5),10**12,10**12,10**12,0.001]

    pose_covariance_matrix = np.ravel(pose_covariance_matrix)

    return (pose_covariance_matrix, twist_covariance_matrix)

def speed_callback(data):
    global vx,vy,vth
    pass

encoder_topic = rospy.get_param('encoder_topic_name','/speed_encoder')
rospy.init_node('odometry_publisher_transform').

odom_pub = rospy.Publisher('/odom', Odometry, queue_size=50)
encoder_sub = rospy.Subscriber(encoder_topic, message, speed_callback)
odom_broadcaster = tf.TransformBroadcaster()

x = 0.0
y = 0.0
th = 0.0

vx = 0.1
vy = -0.1
vth = 0.1

current_time = rospy.Time.now()
last_time = rospy.Time.now()

rate = rospy.Rate(20.0) #publishing at 20Hz

while not rospy.is_shutdown():
    current_time = rospy.Time.now()

    #odometry computation by dead reckoning method
    dt = (current_time - last_time).to_sec() # to find the elapsed time
    delta_x = (vx * cos(th) - vy * sin(th)) * dt
    delta_y = (vx * sin(th) + vy * cos(th)) * dt
    delta_th = vth * dt

    x += delta_x
    y += delta_y
    th += delta_th

    # since all odometry is 6DOF we'll need a quaternion created from yaw
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)

    # first, we'll publish the transform over tf
    odom_broadcaster.sendTransform(
        (x, y, 0.),
        odom_quat,
        current_time,
        "base_link",
        "odom"
    )

    # next, we'll publish the odometry message over ROS
    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    # set the position
    odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

    # set the velocity
    odom.child_frame_id = "base_link"
    odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

    # publish the message
    odom_pub.publish(odom)

    last_time = current_time
    r.sleep()