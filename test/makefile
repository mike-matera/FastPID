
FASTPID_EGG = FastPID-1.0.egg-info 
ARDUINOPID_EGG = ArduinoPID-1.0.egg-info 
AUTOPID_EGG = AutoPID-1.0.egg-info 
PYTHON = python3
PYTEST = pytest -v

all: $(FASTPID_EGG) $(ARDUINOPID_EGG) $(AUTOPID_EGG)

test: $(FASTPID_EGG) $(ARDUINOPID_EGG) $(AUTOPID_EGG)
	$(PYTHON) reference_arduino.py

$(FASTPID_EGG): fastpid_builder.py fastpid_wrapper.cpp ../src/FastPID.cpp ../src/FastPID.h
	CFLAGS="-std=c++11 -DARDUINO=100 -Iemulation" $(PYTHON) fastpid_builder.py 

$(ARDUINOPID_EGG): arduinopid_builder.py arduinopid_wrapper.cpp arduinopid_lib/PID_v1.cpp arduinopid_lib/PID_v1.h
	CFLAGS="-std=c++11 -DARDUINO=100 -I arduinopid_lib -Iemulation" $(PYTHON) arduinopid_builder.py 

$(AUTOPID_EGG): autopid_builder.py autopid_wrapper.cpp autopid_lib/AutoPID.cpp autopid_lib/AutoPID.h
	CFLAGS="-std=c++11 -DARDUINO=100 -I autopid_lib -Iemulation" $(PYTHON) autopid_builder.py 

clean:
	-rm -rf *.so *.egg-info *.png build/ __pycache__ .cache plots

.PHONY: clean
