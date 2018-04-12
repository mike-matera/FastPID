#include "FastPID.h"

#include <Arduino.h>

FastPID::~FastPID() {
}

void FastPID::clear() {
  _last_sp = 0; 
  _last_out = 0;
  _sum = 0; 
  _last_err = 0;
  _last_run = 0;
}

bool FastPID::setCoefficients(float kp, float ki, float kd) {
  _p = floatToParam(kp);
  _i = floatToParam(ki);
  _d = floatToParam(kd);
  return ! _cfg_err;
}

bool FastPID::setDeadband(uint16_t db) {
  if (db != 0 && _i == 0 && _d == 0) {
    // Deadband causes permanent offsets in P controllers.
    // don't let a user do this.
    _db = 0;
    setCfgErr();
    return ! _cfg_err;
  }
  _db = uint32_t(db) * PARAM_MULT;
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

bool FastPID::configure(float kp, float ki, float kd, uint16_t db, int bits, bool sign, bool diff) {
  clear();
  setCoefficients(kp, ki, kd);
  setDeadband(db);
  setOutputConfig(bits, sign, diff);
  return ! _cfg_err; 
}

uint32_t FastPID::floatToParam(float in) {
  if (in > PARAM_MAX || in < 0) {
    _cfg_err = true;
    return 0;
  }
  return in * PARAM_MULT;
}

int16_t FastPID::step(int16_t sp, int16_t fb, uint32_t timestamp) {

  // Calculate delta T
  // millis(): Frequencies less than 1Hz become 1Hz. 
  //   max freqency 1 kHz (XXX: is this too low?)
  uint32_t now;
  if (timestamp != 0) {
    // Let the user specify the sample time. 
    now = timestamp;
  }
  else {
    // Otherwise use the clock
    now = millis();
  }
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
    if (hz == 0) 
      hz = 1;
  }

  _last_run = now;

  // int16 + int16 = int17
  int32_t err = int32_t(sp) - int32_t(fb); 
  int64_t P = 0, I = 0, D = 0;

  if (_p) {
    // uint23 * int16 = int39
    P = int64_t(_p) * int64_t(err);
  }

  if (_i && hz) {
    // int31 + ( int25 *  int17) / int10  = int43
    _sum += (int64_t(_i) * int32_t(err)) / int32_t(hz); 

    // Limit sum to 31-bit signed value so that it saturates, never overflows.
    if (_sum > INTEG_MAX)
      _sum = INTEG_MAX;
    else if (_sum < INTEG_MIN)
      _sum = INTEG_MIN;

    // int43
    I = int64_t(_sum);
  }

  if (_d && hz) {
    // int17 - (int16 - int16) = int19
    int32_t deriv = (sp - _last_sp) - (err - _last_err);
    _last_sp = sp; 
    _last_err = err; 

    // uint23 * int19 * uint16 = int58
    D = int64_t(_d) * int64_t(deriv) * int64_t(hz);
  }

  // int39 (P) + int43 (I) + int58 (D) = int61
  int64_t out = P + I + D;

  // Apply the deadband. 
  if (_db != 0 && out != 0) {
    if (out < 0) {
      if (-out < _db) {
	out = 0;
      }
    }
    else {
      if (out < _db) {
	out = 0;
      }
    }
  }
  
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
