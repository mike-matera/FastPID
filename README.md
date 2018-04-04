# FastPID
A fast fixed-point PID controller for Arduino 

## About 

This PID controller is faster than alternatives for Arduino becuase it avoids expensive floating point operations. The PID controller is configured with floating point coefficients and translates them to fixed point internally. This imposes limitations on the domain of the coefficients. Setting the I and D terms to zero makes the controller run faster. 

## Description of Coefficients 

  * ```Kp``` - P term of the PID controller. 
  * ```Ki``` - I term of the PID controller. 
  * ```Kd``` - D term of the PID controller. 
  * ```db``` - Deadband: the smallest change that can be made in the output of the controller. 

## Input and Output 

The input and the setpoint are an ```int16_t``` this matches the width of Analog pins and accomodate negative readings and setpoints. The output of the PID is an ```int16_t```. The actual bit-width and signedness of the output can be configured. 
  
  * ```bits``` - The output width will be limited to values inside of this bit range. Valid values are 16 through 1 
  * ```sign``` If ```true``` the output range is [-2^(bits-1), -2^(bits-1)-1]. If ```false``` output range is [0, 2^bits-1]

## Time Calculation 

Time is computed automatically each time ```step()``` is called based on ```millis()```. Only PID controllers that use a ```Ki``` and ```Kd``` term rely on time information. 

## Sample Code 

```c++ 
#include <FastPID.h>

#define PIN_INPUT A1
#define PIN_OUTPUT 10

double Kp=0, Ki=0, Kd=1;
uint16_t deadband = 0; 
int output_bits = 8; 
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
  delay(100);
}
```
