/********************************************************
 * PID Basic Example
 * Reading analog input 0 to control analog PWM output 3
 ********************************************************/

#include <FastPID.h>

#define PIN_INPUT A1
#define PIN_OUTPUT 10

double Kp=0, Ki=0, Kd=1;
uint16_t deadband = 0; 
int output_bits = 1; 
bool output_signed = false;

FastPID myPID(Kp, Ki, Kd, deadband, output_bits, output_signed);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int setpoint = 500; 
  int feedback = analogRead(PIN_INPUT);
  int output = myPID.step(setpoint, feedback);
  analogWrite(PIN_OUTPUT, 255 - output);
  Serial.print("sp: "); 
  Serial.print(setpoint); 
  Serial.print(" fb: "); 
  Serial.print(feedback);
  Serial.print(" out: ");
  Serial.println(output);
  delay(100);
}

