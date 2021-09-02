#ifndef _ROS_common_pkg_VisionIn_h
#define _ROS_common_pkg_VisionIn_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/String.h"

namespace common_pkg
{

  class VisionIn : public ros::Msg
  {
    public:
      typedef uint32_t _camera_type;
      _camera_type camera;
      typedef std_msgs::String _mission_type;
      _mission_type mission;
      typedef uint32_t _diceNumber_type;
      _diceNumber_type diceNumber;

    VisionIn():
      camera(0),
      mission(),
      diceNumber(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset + 0) = (this->camera >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->camera >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->camera >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->camera >> (8 * 3)) & 0xFF;
      offset += sizeof(this->camera);
      offset += this->mission.serialize(outbuffer + offset);
      *(outbuffer + offset + 0) = (this->diceNumber >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->diceNumber >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->diceNumber >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->diceNumber >> (8 * 3)) & 0xFF;
      offset += sizeof(this->diceNumber);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      this->camera =  ((uint32_t) (*(inbuffer + offset)));
      this->camera |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->camera |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      this->camera |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      offset += sizeof(this->camera);
      offset += this->mission.deserialize(inbuffer + offset);
      this->diceNumber =  ((uint32_t) (*(inbuffer + offset)));
      this->diceNumber |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->diceNumber |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      this->diceNumber |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      offset += sizeof(this->diceNumber);
     return offset;
    }

    const char * getType(){ return "common_pkg/VisionIn"; };
    const char * getMD5(){ return "a4b734d420413e8a672fa2a29fbdc39a"; };

  };

}
#endif