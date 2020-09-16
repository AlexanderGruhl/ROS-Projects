# ROS-Projects
ROS projects that use ROSPY to program topics, services, and actions in ROS to move robots and read sensor data.

Folder Descriptions:


action_client: ROS action client that sends a goal to the action server in the action_server_example folder to fly the AR-Parrot Drone (https://github.com/AutonomyLab/ardrone_autonomy).

action_server_example: ROS action server that sends the status, result, and feedback to an action client to fly the AR-Parrot Drone.

actions_quiz: Another ROS action server to fly the AR-Parrot Drone.
logger_example_pkg: ROSPY file that shows the various debug messages and allows the programmer to select which level of messages to display in the console.
my_custom_action_msg_pkg: Holds a custom action message.
my_custom_srv_msg_pkg: Holds a custom service message.
my_package: Basic program that sets up a node and runs it infinitely.
my_python_class: Holds Python 3 classes that use ROSPY for a ROS service server and client to move around a BB8 robot model (https://github.com/eborghi10/BB-8-ROS)
my_sphero_actions: Holds a custom action message, the action server and client to move the sphero robot (https://github.com/mmwise/sphero_ros) so it can get out of a maze, and a Python class to run the sphero movement. The action server and client are used for the odometry data of the sphero to check its current postion in the maze and to see if it has left the maze.
my_sphero_topics: ROS topic for collect sphero odometry and IMU data. Using this data the sphero moves.
odometry_package: Folder holds ROS topic subscriber for the ROS odometry message. Folder also holds a custom topic message which publishes the age of the robot.
robot_move: ROS publisher to /cmd_vel topic.
services_quiz: Makes the BB8 robot move in a sqaure using a ROS service server and client.
simple_package: A simple ROS topic publisher that prints a counter variable that updates every 2HZ.
topic_graph: Simple ROS topic subscriber which prints out the value of the INT32 the subscriber gets.
topics_quiz: Using a ROS topic subscriber the program inputs the value of the Kobuki robot's laser scan (https://wiki.ros.org/kobuki) and moves in a certain direction based on the laser scan.
unit_4_services: Uses ROS service server and client to move the BB8 robot in a circle. Holds custom service message.
laser.bag: .bag file which holds recorded scannings from the Kobuki robot.
