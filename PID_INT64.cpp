#include "PID_INT64.h"

#include <iostream>
using namespace std; 

#ifdef ARDUINO 
#define __millis() millis()
#else 
static uint32_t __timer = 0; 
static uint32_t __t() {
  __timer += 1000;
  return __timer;
}
#define __millis() __t()
#endif

PID_INT64::~PID_INT64() {
}

void PID_INT64::clear() {
  _last_sp = 0; 
  _sum = 0; 
  _ctl = 0; 
  _cfg_err = false;
}

bool PID_INT64::configure(float kp, float ki, float kd, float db, int bits, bool sign) {
  clear();
  
  // Set parameters
  _p = floatToParam(kp);
  _i = floatToParam(ki);
  _d = floatToParam(kd);

  // Set deadband 
  if (_i == 0 && _d == 0) {
    // Deadband causes permanent offsets in P controllers. 
    // don't let a user do this. 
    _db = 0; 
  }
  else {
    _db = floatToParam(db);
  }

  // Set output bits
  if (bits > 16 || bits < 1) {
    _cfg_err = true; 
  }
  else {
    if (sign) {
      _outmax = (INT16_MAX << DEC_SHIFT) >> (16 - bits); 
      _outmin = (INT16_MIN << DEC_SHIFT) >> (16 - bits);  
    }
    else {
      _outmax = (UINT16_MAX << DEC_SHIFT) >> (16 - bits); 
      _outmin = 0;
    }
  }

  return !_cfg_err;
}

uint16_t PID_INT64::floatToParam(float in) {
  if (in > PARAM_MAX || in < 0) {
    _cfg_err = true;
    return 0;
  }
  return int16_t(in * PARAM_MULT);
}

int16_t PID_INT64::step(int16_t sp, int16_t fb) {

  // Calculate delta T
  // millis(): Frequencies less than 1Hz are effectively zero. 
  //   max freqency 1 kHz (XXX: is this too low?)
  uint32_t now = __millis();
  uint32_t hz = 0;
  if (_last_run == 0) {
    // Ignore I and D on the first step. They will be 
    // unreliable because no time has really passed.
    hz = 0; 
  }
  else {
    if (now < _last_run) {
      // 47-day timebomb
      hz = uint32_t(1000) / (now + (~_last_run));
    }
    else {
      hz = uint32_t(1000) / (now - _last_run); 
    }
  }

  _last_run = now;

  // int16 + int16 = int17
  int32_t err = int32_t(sp) - int32_t(fb); 
  int64_t P = 0, I = 0, D = 0;

  if (_p) {
    // uint16 * int16 = int32
    P = int64_t(_p) * int64_t(err);
  }

  if (_i && hz) {
    // (int16 * uint32) + int31 = int32
    _sum += int32_t(err) / int32_t(hz); 

    // Limit sum to 31-bit signed value so that it saturates, never overflows.
    if (_sum > INTEG_MAX)
      _sum = INTEG_MAX;
    else if (_sum < INTEG_MIN)
      _sum = INTEG_MIN;

    // uint16 * int31 = int47
    I = int64_t(_i) * int64_t(_sum);
  }

  if (_d && hz) {
    // int17 - (int16 - int16) = int19
    int32_t deriv = (err - _last_err) - (sp - _last_sp);
    _last_sp = sp; 
    _last_err = err; 

    // uint16 * int19 * uint16 = int51
    D = int64_t(_d) * int64_t(deriv) * int64_t(hz);
  }

  // int28 (ctl) + int32 (P) + int47 (I) + int51 (D) = int54
  int64_t diff = P + I + D;

  // Apply the deadband. 
  if (_db) {
    if (diff < 0) {
      if (-diff < _db) {
	diff = 0;
      }
    }
    else {
      if (diff < _db) {
	diff = 0;
      }
    }
  }

  _ctl += diff;

  // Make the output saturate
  if (_ctl > _outmax) 
    _ctl = _outmax;
  else if (_ctl < _outmin) 
    _ctl = _outmin;

  // Remove the integer scaling factor. 
  // int28 >> 13 = int15
  int16_t out = _ctl >> DEC_SHIFT;

  // Fair rounding.
  if (_ctl & (int64_t(0x1) << (DEC_SHIFT - 1))) {
    out++;
  }

  return out;
}


void PID_INT64::setCfgErr() {
  _cfg_err = true;
  _p = _i = _d = 0;
}
