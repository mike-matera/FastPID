
FASTPID_EGG = FastPID-1.0.egg-info 
ARDUINOPID_EGG = ArduinoPID-1.0.egg-info 
AUTOPID_EGG = AutoPID-1.0.egg-info 
PYTHON = python3
PYTEST = pytest -v

all: $(FASTPID_EGG) $(ARDUINOPID_EGG) $(AUTOPID_EGG)

test: $(FASTPID_EGG) $(ARDUINOPID_EGG) $(AUTOPID_EGG)
	$(PYTHON) reference_arduino.py

$(FASTPID_EGG): builder.py wrapper.cpp ../src/FastPID.cpp ../src/FastPID.h
	-rm *.so
	CFLAGS="-std=c++11 -DARDUINO=100 -Iemulation" $(PYTHON) builder.py 

$(ARDUINOPID_EGG): arduino_pid_builder.py arduino_pid_reference.cpp Arduino-PID-Library/PID_v1.cpp Arduino-PID-Library/PID_v1.h
	-rm *.so
	CFLAGS="-std=c++11 -DARDUINO=100 -Iemulation" $(PYTHON) arduino_pid_builder.py 

$(AUTOPID_EGG): auto_pid_builder.py auto_pid_reference.cpp AutoPID/AutoPID.cpp AutoPID/AutoPID.h
	-rm *.so
	CFLAGS="-std=c++11 -DARDUINO=100 -Iemulation" $(PYTHON) auto_pid_builder.py 

clean:
	-rm -rf *.so *.egg-info *.png build/ __pycache__ .cache plots

.PHONY: clean
