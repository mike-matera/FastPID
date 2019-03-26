/*
 * PID Sous-Vide Controller Example.
 *
 * This example shows how to control integral windup in a slow moving system.
 * The heater in a Sous-Vide controller takes considerable time to heat a large
 * volume of water. This causes the integral term to wind up creating an
 * undesirable overshoot before the system comes into regulation. Worse, the
 * overshoot can't be fixed by waiting for the water to warm up then dropping
 * the food in. The temperature deflection caused by dropping cold food into
 * the water will also cause an overshoot.
 *
 * The solution is to use the PID controller only while the temperature is
 * close to the regulation point.
 *
 ********************************************************/

#include <FastPID.h>

#define PIN_INPUT     A0
#define PIN_SETPOINT  A1
#define PIN_OUTPUT    9

float Kp=0.1, Ki=0.5, Kd=0, Hz=10;
int output_bits = 1;
bool output_signed = false;

FastPID myPID(Kp, Ki, Kd, Hz, output_bits, output_signed);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int setpoint = analogRead(PIN_SETPOINT);
  int feedback = analogRead(PIN_INPUT);

  if (feedback < (setpoint * 0.9)) {
    analogWrite(PIN_OUTPUT, 1);
    myPID.clear();
  }
  else {
    analogWrite(PIN_OUTPUT, myPID.step(setpoint, feedback));
  }

  delay(100);
}
