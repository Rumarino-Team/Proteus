#!/bin/bash

python3 /home/nvidia/rumarino_ws/src/sensor_actuator_pkg/scripts/Nodes/SensorNodes/vn100.py &
roslaunch common_pkg StartUp.launch
