
EGG = FastPID-1.0.egg-info 
REF_EGG = ArduinoPID-1.0.egg-info 
PYTHON = python3
PYTEST = pytest -v

all: $(EGG) $(REF_EGG)

test: $(EGG) $(REF_EGG)
	$(PYTHON) reference_arduino.py

$(EGG): builder.py wrapper.cpp ../src/FastPID.cpp ../src/FastPID.h
	-rm *.so
	CFLAGS="-std=c++11" $(PYTHON) builder.py 

$(REF_EGG): arduinopid_builder.py arduino_pid_reference.cpp Arduino-PID-Library/PID_v1.cpp Arduino-PID-Library/PID_v1.h
	-rm *.so
	CFLAGS="-std=c++11 -DARDUINO=100 -Iemulation" $(PYTHON) arduinopid_builder.py 

clean:
	-rm -rf *.so *.egg-info *.png build/ __pycache__ .cache plots

.PHONY: clean
