

http://videohifi17.rssing.com/chan-62314146/all_p49.html

Upgrade Tektronix: FFT analyzer
December 10, 2016, 10:41 am

Okay, I confess: I have a special feeling with Tektronix oscilloscopes. In addition to the 2430A 
recently bought at the market for 50 euros, I already had a 2230 (analog with digital memory) and 
a 4-channel digital TDS420 also taken for two reconditioned money.

Rummaging through the menus of the instrument, I had found an FFT function which however was disabled. 
Searching the net, I discovered that it was an option that could be purchased separately, and that to 
activate it it was necessary to have the internal DSP card with 32MB of RAM. In my instrument there was 
the 16MB card, so I gave up and for a while I didn't think about it anymore.

One day, however, a 32MB card passed by an Australian seller on ebay. Quickly done: bought, paid, 
waited a month, arrived two days ago.

Today I went to work: when I opened the instrument, inside it looks more like a computer than an oscilloscope:

The DSP board to be replaced is the lower one. Note the difference between the two cards: the one with 32MB 
of memory mounts all the DRAM chips, in the other there are empty spaces.

Well, I mount the new card, I try to turn on ... ouch, the FFT function is always disabled. I do not give 
up: a new research on the net leads me to discover that the options cannot be installed simply by mounting 
the new hardware, but must also be enabled in the software by modifying appropriate cells of the configuration 
NVRAM. The modification is done by connecting to a serial service port inside the appliance, a suitable cable 
(non-standard connector) is needed which I prepare in a few minutes, I connect with the hyperterminal, I turn 
on the Teak and the PC messages appear on the PC monitor boot and diagnostics. Once the boot is finished, I 
type the write command in the cell that enables the FFT function, and while there are also the TV synchronization 
processing function (it would come in handy sooner or later ...)

Let's check: the libManagerWordAt (0x50009) command reads the 0x50009 cell which previously contained 0, 
the writing was successful and now returns 1. REBOOT command, the tool restarts, and finally the FFT is enabled. 
Here is the result: the instrument displays a sawtooth signal and its FFT calculated in real time. (Scale: 
12.5KHz / div horizontally and 40dB / div vertically)

It is not a real spectrum analyzer, but something tells me that it will come back VERY useful ... for what 
it cost then (less than 100 euros) it was really worth it.

