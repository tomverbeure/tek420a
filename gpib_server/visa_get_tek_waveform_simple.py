#! /usr/bin/env python3

import pyvisa

# Open a link to device 1 of the GPIB bus
rm = pyvisa.ResourceManager()
g = rm.open_resource('GPIB0::1::INSTR')

# Get the sample points
wf = g.query("CURV?")
print(wf)

