#ifndef PID_INT64_H
#define PID_INT64_H

#include <stdint.h>

#define INTEG_MAX    (INT32_MAX >> 1)
#define INTEG_MIN    (INT32_MIN >> 1)

#define DEC_SHIFT    14
#define PARAM_MAX    (UINT16_MAX >> DEC_SHIFT) 
#define PARAM_MULT   (UINT16_MAX >> (16 - DEC_SHIFT)) 

/*
  A fixed point PID controller with a 64-bit internal calculation pipeline.
*/
class PID_INT64 {

public:
  PID_INT64() : _p(0), _i(0), _d(0), _db(0), 
		_last_sp(0), _last_out(0),
		_sum(0), _last_err(0), _last_run(0), 
		_ctl(0),_outmax(INT16_MAX << 12), _outmin(INT16_MIN << 12),
		_cfg_err(false)
  { 
  }

  PID_INT64(float kp, float ki, float kd, float db=0.0, int bits=16, bool sign=false)
  {
    configure(kp, ki, kd, db, bits, sign);
  }

  ~PID_INT64();

  void clear();
  bool configure(float kp, float ki, float kd, float db=0.0, int bits=16, bool sign=false);
  int16_t step(int16_t sp, int16_t fb);
  bool err() {
    return _cfg_err;
  }

private:

  uint16_t floatToParam(float); 
  void setCfgErr(); 

private:

  uint16_t _p, _i, _d, _db;
  int16_t _last_sp, _last_out;
  int32_t _sum, _last_err;
  uint32_t _last_run; 
  int64_t _ctl, _outmax, _outmin;

  bool _cfg_err; 
};

#endif
