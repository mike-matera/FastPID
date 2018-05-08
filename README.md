# FastPID
A fast 32-bit fixed-point PID controller for Arduino 

## About 

This PID controller is faster than alternatives for Arduino becuase it avoids expensive floating point operations. The PID controller is configured with floating point coefficients and translates them to fixed point internally. This imposes limitations on the domain of the coefficients. Setting the I and D terms to zero makes the controller run faster. The controller is configured to run at a fixed frequency and calling code is responsible for running at that frequency. The ```Ki``` and ```Kd``` parameters are scaled by the frequency to save time during the ```step()``` operation. 

## Description of Coefficients 

  * ```Kp``` - P term of the PID controller. 
  * ```Ki``` - I term of the PID controller. 
  * ```Kd``` - D term of the PID controller. 
  * ```Hz``` - The execution frequency of the controller. 

### Coefficient Domain 

The computation pipeline expects 16 bit coefficients. This is controlled by ``PARAM_BITS`` and should not be changed or caluclations may overflow. The number of bits before and after the decimal place is controlled by ``PARAM_SHIFT`` in FastPID.h. The default value for ``PARAM_SHIFT`` is 8.

  **The parameter P domain is [0.00390625 to 255] inclusive.** 
  **The parameter I domain is P / Hz** 
  **The parameter D domain is P * Hz** 

The controller checks for parameter domain violations and won't operate if a coefficient is outside of the range. All of the configuration operations return ```bool``` to alert the user of an error. The ```err()``` function checks the error condition. Errors can be cleared with the ```clear()``` function.

## Execution Frequency

**The execution frequency is not automatically detected as of version v1.1.0** This greatly improves the controller performance. Instead the '''Ki''' and '''Kd''' terms are scaled in the configuration step. It's essential to call '''step()''' at the rate that you specify. 

## Input and Output 

The input and the setpoint are an ```int16_t``` this matches the width of Analog pins and accomodate negative readings and setpoints. The output of the PID is an ```int16_t```. The actual bit-width and signedness of the output can be configured. 
  
  * ```bits``` - The output width will be limited to values inside of this bit range. Valid values are 1 through 16 
  * ```sign``` If ```true``` the output range is [-2^(bits-1), -2^(bits-1)-1]. If ```false``` output range is [0, 2^(bits-1)-1]. **The maximum output value of the controller is 32767 (even in 16 bit unsigned mode)** 

## Sample Code 

```c++ 
#include <FastPID.h>

#define PIN_INPUT     A0
#define PIN_SETPOINT  A1
#define PIN_OUTPUT    9

float Kp=0.1, Ki=0.5, Kd=0, Hz=10;
int output_bits = 8;
bool output_signed = false;

FastPID myPID(Kp, Ki, Kd, Hz, output_bits, output_signed);

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
