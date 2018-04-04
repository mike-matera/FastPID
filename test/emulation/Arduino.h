#include <iostream>
#include <stdint.h>
using namespace std;
static uint32_t __timer = 0; 
static uint32_t __t() {
  __timer += 1000;
  return __timer;
}
#define millis() __t()
