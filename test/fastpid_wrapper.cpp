#include <Python.h>
#include "FastPID.h"

FastPID pid; 

static PyObject *
configure(PyObject *self, PyObject *args) {
  float kp;
  float ki;
  float kd; 
  int bits=16; 
  bool sign=false;

  if (!PyArg_ParseTuple(args, "fffib", &kp, &ki, &kd, &bits, &sign))
    return NULL;

  return PyBool_FromLong(pid.configure(kp, ki, kd, 1, bits, sign));
}

static PyObject *
step(PyObject *self, PyObject *args) {
  int sp; 
  int err;
  if (!PyArg_ParseTuple(args, "ii", &sp, &err))
    return NULL;

  return PyLong_FromLong(pid.step(sp, err));
}

static PyMethodDef PIDMethods[] = {
    {"configure",  configure, METH_VARARGS, "Configure the PID."},
    {"step",  step, METH_VARARGS, "Run a PID step."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pid_module = {
   PyModuleDef_HEAD_INIT,
   "FastPID",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
   PIDMethods
};

PyMODINIT_FUNC
PyInit_FastPID(void)
{
  return PyModule_Create(&pid_module);
}
