#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf_conversions
## END_SUB_TUTORIAL

from std_msgs.msg import String
from std_srvs.srv import Empty
from moveit_msgs.msg import Constraints, OrientationConstraint
from warehouse_python_interface.srv import *
from set_gripper_state.srv import SetGripperState
from motoman_msgs.srv import *
from motoman_msgs.msg import *

switchonservice = 0
switchoffservice = 0

def handle_motoman_gripper(state):
    print state
    global switchonservice
    global switchoffservice
    rospy.loginfo("CALLBACK")
    if state.value == 1 and state.address == 10010:
      # off
      switchoffservice()
      return WriteSingleIOResponse()

    if state.value == 0 and state.address == 10010:
      # on
      switchonservice()
      return WriteSingleIOResponse()

    return WriteSingleIOResponse()

def gripper():
    rospy.init_node('gazebo_gripper_wrapper')

    rospy.loginfo("load")
    global switchonservice
    global switchoffservice
    switchonservice = rospy.ServiceProxy('/motoman_sia10f/vacuum_gripper/on', Empty)
    switchoffservice = rospy.ServiceProxy('/motoman_sia10f/vacuum_gripper/off', Empty)

    s = rospy.Service('write_single_io', WriteSingleIO, handle_motoman_gripper)
    rospy.loginfo("ready to receive vacuum commands")
    rospy.spin()

if __name__ == "__main__":
    gripper()
