#!/usr/bin/python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from numpy import arctan2

x = 0
y = 0
theta = 0

def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")
sub = rospy.Subscriber("/car/diff_drive_controller/odom", Odometry, newOdom)
pub = rospy.Publisher("/car/diff_drive_controller/cmd_vel", Twist, queue_size = 1)

speed = Twist()

goal = Point()
goal.x = 4
goal.y = 2

def goTo(goal):
    global x
    global y
    global theta
    global sub
    global pub
    global speed

    arrived = False
    while not arrived:
        inc_x = goal.x -x
        inc_y = goal.y -y
        angle_to_goal = arctan2(inc_y, inc_x)

        if angle_to_goal > 0:
            val = 0.25
        else:
            val = -0.25

        if abs(angle_to_goal - theta) > 0.25:
            speed.angular.z = val
            speed.linear.x = 0.0
        else:
            speed.linear.x = 1.0
            speed.angular.z = 0.0

        if abs(inc_x) <1 and abs(inc_y)< 1:
        	arrived = True
        	print("destination reached!")
        pub.publish(speed)


goTo(goal)
a = int(input("want to go back ? (0/1)  "))
if (a == 1):
    goal.x = 0
    goal.y = 0
    goTo(goal)
