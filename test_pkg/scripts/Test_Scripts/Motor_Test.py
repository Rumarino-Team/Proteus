import sys
import signal
import Utils
import rospy
from std_msgs.msg import Int32
from controller_pkg.msg import HorizontalMotors
from Utils import get_input, wait_for_enter


class Motor_Test:
    def __init__(self):
        # ##########Calibration Box########## #
        self.vertical_motor_count = 4
        self.horizontal_motor_count = 2
        # ################################### #

        self.report = []
        self.vm = rospy.Publisher("vertical_motors", Int32, queue_size=10)
        self.hm = rospy.Publisher("horizontal_motors", HorizontalMotors, queue_size=10)
        self.motor_speed = 0
        self.motor_names = ["Front Right", "Front Left", "Back Right", "Back Left"]

    def get_speed(self):
        finished = False
        while not finished:
            try:
                inp = int(get_input("Please enter an integer for motor testing speed: "))
                self.motor_speed = inp
                finished = True
            except ValueError:
                print("PLEASE ENTER A VALID INTEGER!")
        return self.motor_speed

    def test_vertical_motor(self, motor_number, motor_speed):
        arr = [0, 0, 0, 0]
        arr[motor_number] = motor_speed
        self.vm.publish(*arr)
        message = self.motor_names[motor_number] + " Motor: " + str(motor_number)
        print(message)
        is_on = get_input("Is motor on? (y/n): ")
        is_clockwise = get_input("Is motor turning clockwise? (y/n): ")
        self.vm.publish(0, 0, 0, 0)
        entry = (message, is_on, is_clockwise)
        self.report.append(entry)

    def test_horizontal_motor(self, motor_number, motor_speed):  # both test functions could be merged
        arr = [0, 0]
        arr[motor_number] = motor_speed
        self.vm.publish(*arr)
        message = self.motor_names[motor_number] + "Motor: " + str(motor_number)
        print(message)
        is_on = get_input("Is motor on? (y/n): ")
        is_clockwise = get_input("Is motor turning clockwise? (y/n): ")
        self.hm.publish(0, 0)
        entry = (message, is_on, is_clockwise)
        self.report.append(entry)

    def get_report(self):
        return self.report

    def run_test(self):
        print("Motor Test Started:")
        speed = self.get_speed()
        print("Testing Vertical Motors...")
        wait_for_enter()
        for vertical_motor in range(0, self.vertical_motor_count):
            self.test_vertical_motor(vertical_motor, speed)
        print("Testing Horizontal Motors...")
        print("Please stand behind the AUV...")
        wait_for_enter()
        for horizontal_motor in range(0, self.horizontal_motor_count):
            self.test_horizontal_motor(horizontal_motor, speed)
        print("Motor Test concluded")
        wait_for_enter()
        return self.report

