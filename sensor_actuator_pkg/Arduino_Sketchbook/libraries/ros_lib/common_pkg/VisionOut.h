#ifndef _ROS_common_pkg_VisionOut_h
#define _ROS_common_pkg_VisionOut_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace common_pkg
{

  class VisionOut : public ros::Msg
  {
    public:
      typedef uint32_t _centroid_x_type;
      _centroid_x_type centroid_x;
      typedef uint32_t _centroid_y_type;
      _centroid_y_type centroid_y;

    VisionOut():
      centroid_x(0),
      centroid_y(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset + 0) = (this->centroid_x >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->centroid_x >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->centroid_x >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->centroid_x >> (8 * 3)) & 0xFF;
      offset += sizeof(this->centroid_x);
      *(outbuffer + offset + 0) = (this->centroid_y >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->centroid_y >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->centroid_y >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->centroid_y >> (8 * 3)) & 0xFF;
      offset += sizeof(this->centroid_y);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      this->centroid_x =  ((uint32_t) (*(inbuffer + offset)));
      this->centroid_x |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->centroid_x |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      this->centroid_x |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      offset += sizeof(this->centroid_x);
      this->centroid_y =  ((uint32_t) (*(inbuffer + offset)));
      this->centroid_y |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->centroid_y |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      this->centroid_y |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      offset += sizeof(this->centroid_y);
     return offset;
    }

    const char * getType(){ return "common_pkg/VisionOut"; };
    const char * getMD5(){ return "22e2d756b5915264467c65d1ff54e3bf"; };

  };

}
#endif