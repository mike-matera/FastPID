
EGG = PID_INT64-1.0.egg-info 
PYTHON = python3
PYTEST = pytest -v

all: test

test: $(EGG)
	$(PYTHON) reference.py

$(EGG): builder.py wrapper.cpp ../PID_INT64.cpp ../PID_INT64.h
	$(PYTHON) builder.py 

clean:
	-rm -rf *.so *.egg-info *.png build/ __pycache__ .cache

.PHONY: clean
