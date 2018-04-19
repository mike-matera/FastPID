# FastPID
A fast fixed-point PID controller for Arduino 

## About 

This PID controller is faster than alternatives for Arduino becuase it avoids expensive floating point operations. The PID controller is configured with floating point coefficients and translates them to fixed point internally. This imposes limitations on the domain of the coefficients. Setting the I and D terms to zero makes the controller run faster. 

## Description of Coefficients 

  * ```Kp``` - P term of the PID controller. 
  * ```Ki``` - I term of the PID controller. 
  * ```Kd``` - D term of the PID controller. 

### Coefficient Domain 

The computation pipeline expects 25 bit coefficients. This is controlled by ``PARAM_BITS`` and cannot be changed without breaking the controller. The number of bits before and after the decimal place is controlled by ``PARAM_SHIFT`` in FastPID.h. The default value for ``PARAM_SHIFT`` is 15.

  **The parameter domain is [1023 to 0.00006103515625] inclsive** 
  
## Input and Output 

The input and the setpoint are an ```int16_t``` this matches the width of Analog pins and accomodate negative readings and setpoints. The output of the PID is an ```int16_t```. The actual bit-width and signedness of the output can be configured. 
  
  * ```bits``` - The output width will be limited to values inside of this bit range. Valid values are 16 through 1 
  * ```sign``` If ```true``` the output range is [-2^(bits-1), -2^(bits-1)-1]. If ```false``` output range is [0, 2^bits-1]

If you're using an unsigned type as an output be sure to cast the output so you don't inadvertantly get a negative value. 

## Time Calculation 

Time is computed automatically each time ```step()``` is called based on ```millis()```. Only PID controllers that use a ```Ki``` and ```Kd``` term rely on time information. You must control the rate at which the controller is called. Unlike ArduinoPID calling ``step()`` will always do a calculation, no matter how much time has passed. 

## Sample Code 

```c++ 
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
```
