
EGG = FastPID-1.0.egg-info 
PYTHON = python3
PYTEST = pytest -v

all: $(EGG)

test: $(EGG)
	$(PYTHON) reference.py

$(EGG): builder.py wrapper.cpp ../src/FastPID.cpp ../src/FastPID.h
	-rm *.so
	$(PYTHON) builder.py 

clean:
	-rm -rf *.so *.egg-info *.png build/ __pycache__ .cache plots

.PHONY: clean
