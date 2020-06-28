#! /usr/bin/env python3

import pyvisa

#rm = pyvisa.ResourceManager('@py')
rm = pyvisa.ResourceManager()
#print(rm.list_resources())

#siglent = rm.open_resource("TCPIP::192.168.1.177")
#siglent = rm.open_resource("USB0::0xF4EC::0xEE3A7:SDS2XJBD1R2754")
#print(siglent.query('*IDN?'))

g = rm.open_resource('GPIB0::1::INSTR')
print(g.query('*IDN?'))
print(g.query('*LRN?'))
