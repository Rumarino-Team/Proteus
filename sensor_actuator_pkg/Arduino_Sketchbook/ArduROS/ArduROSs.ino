#include <Arduino.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Float32.h>
#include <controller_pkg/HorizontalMotors.h>
#include <controller_pkg/VerticalMotors.h>
#include <Motors.h>
#include <Wire.h>
#include <blue_robotics.h>
#include <Servo.h>


std_msgs::Float32 depth;
MS5837 pressureSensor;


// Callback function for left motors
void setHorizontalMotors(const controller_pkg::HorizontalMotors&  motorIntensity)
{
   setHorizontalMotorSpeed(motorIntensity.rightMotor, motorIntensity.leftMotor);
}

// Callback function for simultaneous usage of motors
void setVerticalMotors(const controller_pkg::VerticalMotors& motorIntensity)
{
    setVerticalMotorSpeed(motorIntensity.frontRight, motorIntensity.frontLeft, motorIntensity.backRight, motorIntensity.backLeft);
}
//declaring node nh of type NodeHandle
ros::NodeHandle nh;

// Creates all the ROS subscriber objects 
ros::Subscriber<controller_pkg::VerticalMotors> subVerticalMotors("vertical_motors", setVerticalMotors);
ros::Subscriber<controller_pkg::HorizontalMotors> subHorizontalMotors("horizontal_motors", setHorizontalMotors);

// Create the pressure sensor publisher object
// Object named pubTpoPressureSensor of type Publisher
//params: topic name 
//        topic type
ros::Publisher pubToPressureSensor("depth_current", &depth);


void setup() {
  // Initializes the node and prepares for publishing and subscribing.
  //nh fuctions required for the nh to fuction
  nh.initNode();//initializes node
  nh.advertise(pubToPressureSensor);                                       //Declares pubToPressureSensor as a Publisher
  nh.subscribe(subVerticalMotors);                                         //Declares pubToPressureSensor as a Subscriber
  nh.subscribe(subHorizontalMotors);                                       //Declares pubToPressureSensor as a Subscriber

  // Initializes all the motors
  initializeVerticalMotors();
  initializeHorizontalMotors("old");

  //Initializes wire (protocol to run) initializes the serial communication
  Wire.begin(); 

  // If pressure sensor does not initialize, throw error
 
  while(!pressureSensor.init())
  {
      
      nh.logerror("Pressure sensor cannot initialize.");
      
  }

}

void loop() 
{
  
  pressureSensor.read();                                      //funtion within pressure sensor object that gives the values the sensor is reading
  
  depth.data = pressureSensor.depth()*(3.3);                  //3.3 is a convesion from meter to feet
    
  pubToPressureSensor.publish(&depth);
  
  nh.spinOnce();                                              //Makes sure that rose knows this is a loop
}
