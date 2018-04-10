#include <Python.h>
#include "AutoPID.h"
#include <iostream>

double Setpoint, Input, Output;

AutoPID pid(&Input, &Setpoint, &Output, 0, 0, 0, 0, 0);

static PyObject *
configure(PyObject *self, PyObject *args) {
  float kp;
  float ki;
  float kd; 
  int bits=16; 
  bool sign=false;
  
  if (!PyArg_ParseTuple(args, "fffib", &kp, &ki, &kd, &bits, &sign))
    return NULL;

  int64_t outmax, outmin;
  if (bits > 16 || bits < 1) {
    return PyBool_FromLong(false);
  }  
  else {
    if (sign) {
      outmax = ((0x1ULL << (bits - 1)) - 1);
      outmin = -((0x1ULL << (bits - 1)));
    }
    else {
      outmax = ((0x1ULL << bits) - 1);
      outmin = 0;
    }
  }

  pid.setGains(kp, ki, kd);
  pid.setTimeStep(1000); 
  pid.setOutputRange(outmin, outmax);
  return PyBool_FromLong(true);
}

static PyObject *
step(PyObject *self, PyObject *args) {
  int sp; 
  int fb;
  if (!PyArg_ParseTuple(args, "ii", &sp, &fb))
    return NULL;

  Setpoint = sp;
  Input = fb; 
  pid.run();
  return PyLong_FromLong(Output);
}

static PyMethodDef PIDMethods[] = {
    {"configure",  configure, METH_VARARGS, "Configure the PID."},
    {"step",  step, METH_VARARGS, "Run a PID step."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pid_module = {
   PyModuleDef_HEAD_INIT,
   "AutoPID",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
   PIDMethods
};

PyMODINIT_FUNC
PyInit_AutoPID(void)
{
  return PyModule_Create(&pid_module);
}
