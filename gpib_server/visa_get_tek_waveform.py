#! /usr/bin/env python3

import pyvisa
import sys

rm = pyvisa.ResourceManager()
g = rm.open_resource('GPIB0::1::INSTR')

# Query scope identification
print("*IDN?: %s" % g.query("*IDN?"))

# Setup a single sequence acquisition
g.write("ACQ:STOPA SEQ")

# Don't do repetitive acquisition (~equivalent-time operation)
g.write("ACQ:REPE OFF")

# Start acquiring data
g.write("ACQ:STATE RUN")

# Record 500 waveform samples
g.write("HOR:RECORDL 500");

# Encode the waveform as a comma-separated list
g.write("DATA:ENC ASCI")

# Request data from channel 1 only
g.write("DATA:SOURCE CH1")

# Get all waveform acquisition settings needed decode the sample points values: vdiv, number of sample points etc.
print(g.query("WFMPRE?"))

# Get the sample points
print(g.query("CURV?"))

