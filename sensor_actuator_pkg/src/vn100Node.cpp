#include <iostream>
#include "ros/ros.h"
#include <std_msgs/Float32.h>
#include "vn/ezasyncdata.h"

using namespace std;
using namespace vn::sensors;
using namespace vn::math;
using namespace vn::protocol::uart;
using namespace vn::xplat;

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "vn100");
    ros::NodeHandle n;
    ros::Rate loop_rate(10);
    ros::Publisher vn100_pub = n.advertise<std_msgs::Float32>("yaw_current", 10);
	const string SensorPort = "/dev/ttyUSB0";
	const uint32_t SensorBaudrate = 115200;

	EzAsyncData* ez = EzAsyncData::connect(SensorPort, SensorBaudrate);
    std_msgs::Float32 current_angle;
	while (ros::ok())
	{
		CompositeData cd = ez->getNextData();

		if (!cd.hasYawPitchRoll())
			cout << "YPR Unavailable " << endl;
		else
        {
            current_angle.data = cd.yawPitchRoll()[0];
            if(current_angle.data < 0)
                current_angle.data +=360;
			vn100_pub.publish(current_angle);
        }
        loop_rate.sleep();
	}

	ez->disconnect();

	delete ez;

	return 0;
}