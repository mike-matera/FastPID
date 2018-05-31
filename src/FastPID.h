#ifndef FastPID_H
#define FastPID_H

#include <stdint.h>

#define INTEG_MAX    (INT32_MAX)
#define INTEG_MIN    (INT32_MIN)
#define DERIV_MAX    (INT16_MAX)
#define DERIV_MIN    (INT16_MIN)

#define PARAM_SHIFT  8
#define PARAM_BITS   16
#define PARAM_MAX    (((0x1ULL << PARAM_BITS)-1) >> PARAM_SHIFT) 
#define PARAM_MULT   (((0x1ULL << PARAM_BITS)) >> (PARAM_BITS - PARAM_SHIFT)) 

/*
  A fixed point PID controller with a 32-bit internal calculation pipeline.
*/
class FastPID {

public:
  FastPID() 
  {
    clear();
  }

  FastPID(float kp, float ki, float kd, float hz, int bits=16, bool sign=false)
  {
    configure(kp, ki, kd, hz, bits, sign);
  }

  ~FastPID();

  bool setCoefficients(float kp, float ki, float kd, float hz);
  bool setOutputConfig(int bits, bool sign);
  bool setOutputRange(int16_t min, int16_t max);
  void clear();
  bool configure(float kp, float ki, float kd, float hz, int bits=16, bool sign=false);
  int16_t step(int16_t sp, int16_t fb);

  bool err() {
    return _cfg_err;
  }

private:

  uint32_t floatToParam(float); 
  void setCfgErr(); 

private:

  // Configuration
  uint32_t _p, _i, _d;
  int64_t _outmax, _outmin; 
  bool _cfg_err; 
  
  // State
  int16_t _last_sp, _last_out;
  int64_t _sum;
  int32_t _last_err;
};

#endif
