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

bool FastPID::setOutputConfig(int bits, bool sign) {
  // Set output bits
  if (bits > 16 || bits < 1) {
    setCfgErr();
  }
  else {
    if (bits == 16) {
      _outmax = (0xFFFFULL >> (17 - bits)) * PARAM_MULT;
    }
    else{
      _outmax = (0xFFFFULL >> (16 - bits)) * PARAM_MULT;
    }
    if (sign) {
      _outmin = -((0xFFFFULL >> (17 - bits)) + 1) * PARAM_MULT;
    }
    else {
      _outmin = 0;
    }
  }
  return ! _cfg_err;
}

bool FastPID::setOutputRange(int16_t min, int16_t max)
{
  if (min >= max) {
    setCfgErr();
    return ! _cfg_err;
  }
  _outmin = int64_t(min) * PARAM_MULT;
  _outmax = int64_t(max) * PARAM_MULT;
  return ! _cfg_err;
}

bool FastPID::configure(float kp, float ki, float kd, float hz, int bits, bool sign) {
  clear();
  setCoefficients(kp, ki, kd, hz);
  setOutputConfig(bits, sign);
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
  int32_t P = 0, I = 0;
  int32_t D = 0;

  if (_p) {
    // uint16 * int16 = int32
    P = int32_t(_p) * int32_t(err);
  }

  if (_i) {
    // int17 * int16 = int33
    _sum += int64_t(err) * int64_t(_i);

    // Limit sum to 32-bit signed value so that it saturates, never overflows.
    if (_sum > INTEG_MAX)
      _sum = INTEG_MAX;
    else if (_sum < INTEG_MIN)
      _sum = INTEG_MIN;

    // int32
    I = _sum;
  }

  if (_d) {
    // (int17 - int16) - (int16 - int16) = int19
    int32_t deriv = (err - _last_err) - int32_t(sp - _last_sp);
    _last_sp = sp; 
    _last_err = err; 

    // Limit the derivative to 16-bit signed value.
    if (deriv > DERIV_MAX)
      deriv = DERIV_MAX;
    else if (deriv < DERIV_MIN)
      deriv = DERIV_MIN;

    // int16 * int16 = int32
    D = int32_t(_d) * int32_t(deriv);
  }

  // int32 (P) + int32 (I) + int32 (D) = int34
  int64_t out = int64_t(P) + int64_t(I) + int64_t(D);

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
