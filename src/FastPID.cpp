#include "FastPID.h"

#include <Arduino.h>

FastPID::~FastPID() {
}

void FastPID::clear() {
  _last_sp = 0; 
  _last_out = 0;
  _sum = 0; 
  _last_err = 0;
  _cfg_err = false;
} 

bool FastPID::setCoefficients(float kp, float ki, float kd, float hz) {
  _p = floatToParam(kp);
  _i = floatToParam(ki / hz);
  _d = floatToParam(kd * hz);
  return ! _cfg_err;
}

bool FastPID::setOutputConfig(int bits, bool sign, bool differential) {
  // Set output bits
  if (bits > 16 || bits < 1) {
    _cfg_err = true; 
  }
  else {
    if (sign) {
      _outmax = ((0x1ULL << (bits - 1)) - 1) * PARAM_MULT;
      _outmin = -((0x1ULL << (bits - 1))) * PARAM_MULT;
    }
    else {
      _outmax = ((0x1ULL << bits) - 1) * PARAM_MULT;
      _outmin = 0;
    }
  }
  _differential = differential;
  return ! _cfg_err;
}

bool FastPID::configure(float kp, float ki, float kd, float hz, int bits, bool sign, bool diff) {
  clear();
  setCoefficients(kp, ki, kd, hz);
  setOutputConfig(bits, sign, diff);
  return ! _cfg_err; 
}

uint32_t FastPID::floatToParam(float in) {
  if (in > PARAM_MAX || in < 0) {
    _cfg_err = true;
    return 0;
  }

  uint32_t param = in * PARAM_MULT;

  if (in != 0 && param == 0) {
    _cfg_err = true;
    return 0;
  }
  
  return param;
}

int16_t FastPID::step(int16_t sp, int16_t fb) {

  // int16 + int16 = int17
  int32_t err = int32_t(sp) - int32_t(fb); 
  int64_t P = 0, I = 0, D = 0;

  if (_p) {
    // uint23 * int16 = int39
    P = int64_t(_p) * int64_t(err);
  }

  if (_i) {
    // XXX: int31 + (int25 * int17) = int32
    _sum += int64_t(_i) * int32_t(err);

    // Limit sum to 31-bit signed value so that it saturates, never overflows.
    if (_sum > INTEG_MAX)
      _sum = INTEG_MAX;
    else if (_sum < INTEG_MIN)
      _sum = INTEG_MIN;

    // int43
    I = int64_t(_sum);
  }

  if (_d) {
    // int17 - (int16 - int16) = int19
    int32_t deriv = (err - _last_err) - (sp - _last_sp);
    _last_sp = sp; 
    _last_err = err; 

    // XXX: uint25 * int19 = int44
    D = int64_t(_d) * int64_t(deriv);
  }

  // int39 (P) + int43 (I) + int44 (D) = int45
  int64_t out = P + I + D;
  
  // Make the output saturate
  if (out > _outmax) 
    out = _outmax;
  else if (out < _outmin) 
    out = _outmin;

  // Remove the integer scaling factor. 
  int16_t rval = out >> PARAM_SHIFT;

  // Fair rounding.
  if (out & (0x1ULL << (PARAM_SHIFT - 1))) {
    rval++;
  }

  return rval;
}

void FastPID::setCfgErr() {
  _cfg_err = true;
  _p = _i = _d = 0;
}
