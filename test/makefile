
EGG = PID_INT64-1.0.egg-info 
PYTHON = python3

all: $(EGG)

$(EGG): builder.py wrapper.cpp ../PID_INT64.cpp ../PID_INT64.h
	$(PYTHON) builder.py 

clean:
	-rm -rf *.so *.egg-info build/ 

.PHONY: clean
