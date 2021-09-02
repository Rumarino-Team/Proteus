#ifndef _ROS_controller_pkg_ForwardsCommand_h
#define _ROS_controller_pkg_ForwardsCommand_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace controller_pkg
{

  class ForwardsCommand : public ros::Msg
  {
    public:
      typedef int32_t _motorIntensity_type;
      _motorIntensity_type motorIntensity;
      typedef bool _movingForwards_type;
      _movingForwards_type movingForwards;

    ForwardsCommand():
      motorIntensity(0),
      movingForwards(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_motorIntensity;
      u_motorIntensity.real = this->motorIntensity;
      *(outbuffer + offset + 0) = (u_motorIntensity.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_motorIntensity.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_motorIntensity.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_motorIntensity.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->motorIntensity);
      union {
        bool real;
        uint8_t base;
      } u_movingForwards;
      u_movingForwards.real = this->movingForwards;
      *(outbuffer + offset + 0) = (u_movingForwards.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->movingForwards);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_motorIntensity;
      u_motorIntensity.base = 0;
      u_motorIntensity.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_motorIntensity.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_motorIntensity.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_motorIntensity.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->motorIntensity = u_motorIntensity.real;
      offset += sizeof(this->motorIntensity);
      union {
        bool real;
        uint8_t base;
      } u_movingForwards;
      u_movingForwards.base = 0;
      u_movingForwards.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->movingForwards = u_movingForwards.real;
      offset += sizeof(this->movingForwards);
     return offset;
    }

    const char * getType(){ return "controller_pkg/ForwardsCommand"; };
    const char * getMD5(){ return "280d8b4e9b069d35879962bdb25e6da1"; };

  };

}
#endif