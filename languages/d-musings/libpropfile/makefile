#
# Makefile for libpropfile project

all: propfile.a test01

propfile.a: cm2c/propfile.d
	dmd -lib cm2c/propfile.d
	
test01: test01.d propfile.a
	dmd -Lpropfile.a test01.d
	
clean:
	-rm propfile.a
	-rm test01