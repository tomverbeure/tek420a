#! /usr/bin/env python3

import pyvisa
import sys

rm = pyvisa.ResourceManager('@py')
#rm = pyvisa.ResourceManager()
print(rm.list_resources())

#siglent = rm.open_resource("TCPIP::192.168.1.177")
#siglent = rm.open_resource("USB0::0xF4EC::0xEE3A7:SDS2XJBD1R2754")
#print(siglent.query('*IDN?'))

g = rm.open_resource('GPIB0::1::INSTR')
#g = rm.open_resource('GPIB0::29::INSTR')
#print(g.query('*IDN?'))

print(sys.argv[1])
g.write(sys.argv[1])
print(g.read())
