#ifndef _ROS_controller_pkg_VerticalMotors_h
#define _ROS_controller_pkg_VerticalMotors_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace controller_pkg
{

  class VerticalMotors : public ros::Msg
  {
    public:
      typedef int32_t _frontRight_type;
      _frontRight_type frontRight;
      typedef int32_t _frontLeft_type;
      _frontLeft_type frontLeft;
      typedef int32_t _backRight_type;
      _backRight_type backRight;
      typedef int32_t _backLeft_type;
      _backLeft_type backLeft;

    VerticalMotors():
      frontRight(0),
      frontLeft(0),
      backRight(0),
      backLeft(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_frontRight;
      u_frontRight.real = this->frontRight;
      *(outbuffer + offset + 0) = (u_frontRight.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_frontRight.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_frontRight.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_frontRight.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->frontRight);
      union {
        int32_t real;
        uint32_t base;
      } u_frontLeft;
      u_frontLeft.real = this->frontLeft;
      *(outbuffer + offset + 0) = (u_frontLeft.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_frontLeft.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_frontLeft.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_frontLeft.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->frontLeft);
      union {
        int32_t real;
        uint32_t base;
      } u_backRight;
      u_backRight.real = this->backRight;
      *(outbuffer + offset + 0) = (u_backRight.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_backRight.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_backRight.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_backRight.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->backRight);
      union {
        int32_t real;
        uint32_t base;
      } u_backLeft;
      u_backLeft.real = this->backLeft;
      *(outbuffer + offset + 0) = (u_backLeft.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_backLeft.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_backLeft.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_backLeft.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->backLeft);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_frontRight;
      u_frontRight.base = 0;
      u_frontRight.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_frontRight.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_frontRight.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_frontRight.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->frontRight = u_frontRight.real;
      offset += sizeof(this->frontRight);
      union {
        int32_t real;
        uint32_t base;
      } u_frontLeft;
      u_frontLeft.base = 0;
      u_frontLeft.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_frontLeft.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_frontLeft.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_frontLeft.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->frontLeft = u_frontLeft.real;
      offset += sizeof(this->frontLeft);
      union {
        int32_t real;
        uint32_t base;
      } u_backRight;
      u_backRight.base = 0;
      u_backRight.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_backRight.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_backRight.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_backRight.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->backRight = u_backRight.real;
      offset += sizeof(this->backRight);
      union {
        int32_t real;
        uint32_t base;
      } u_backLeft;
      u_backLeft.base = 0;
      u_backLeft.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_backLeft.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_backLeft.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_backLeft.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->backLeft = u_backLeft.real;
      offset += sizeof(this->backLeft);
     return offset;
    }

    const char * getType(){ return "controller_pkg/VerticalMotors"; };
    const char * getMD5(){ return "6d840ac65c3a0bb8fd0256a7c238f503"; };

  };

}
#endif