/*
 * PID Voltage Regulator Example. 
 * 
 * See the accompaning circuit in VoltageRegulator.png. 
 * The circuit is a very poor regulator that's complex
 * and nonlinear. A good example to show PID tuning. 
 * 
 * If connected correctly the LED shows the approximate
 * output of the system. The brightness should respond
 * to the dial. Check the serial port to see what the 
 * actual system values are. 
 * 
 ********************************************************/

#include <FastPID.h>

#define PIN_INPUT     A0
#define PIN_SETPOINT  A1
#define PIN_OUTPUT    9

float Kp=0.1, Ki=0.5, Kd=0;
int output_bits = 8;
bool output_signed = false;

FastPID myPID(Kp, Ki, Kd, output_bits, output_signed);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int setpoint = analogRead(PIN_SETPOINT) / 2; 
  int feedback = analogRead(PIN_INPUT);
  uint8_t output = myPID.step(setpoint, feedback);
  analogWrite(PIN_OUTPUT, output);
  Serial.print("sp: "); 
  Serial.print(setpoint); 
  Serial.print(" fb: "); 
  Serial.print(feedback);
  Serial.print(" out: ");
  Serial.println(output);
  delay(100);
}

