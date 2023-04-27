### ROS package that determines the probability of a social humanoid robot's expression during an interaction with a child

#### After running the launch file,  numerical predictions should be published on each of the 4 ROS topics (i.e. a different prediction every 10 seconds).

#### To run the package:

1.) Download and unzip the attached package into your catkin workspace,

2.) Run the 'source /opt/ros/noetic/setup.bash'and '. ~/catkin_ws/devel/setup.bash' command from the now opened catkin workspace. Take note to do this for every newly opened terminal

3.) Run the 'catkin_make' command from the same workspace

4.) Run the 'roscore'command from a new terminal,

5.) Once the workspace is ready, make all the nodes executable by running the commands below from the "scripts" folder containing all the nodes in the terminal where 'catkin_make' command was run:

  'chmod +x interaction_generator.py
   chmod +x perceived_info.py
   chmod +x robot_controller.py
   chmod +x robot_expression_prediciton.py'

6.) Launch the package by running:

  'roslaunch cr_week6_test human_robot_interaction.launch'

7.) Run 'rqt_graph' in a new terminal to get the visual representation of the package

### List of Dependencies:

- python 3.8.10
- ros-noetic
- Numpy
- CMake
