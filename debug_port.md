
https://forum.tek.com/viewtopic.php?t=138100

TDS 420 Debug Serial Port
Quote
Post  by mirco » November 22nd, 2014, 3:43 pm

Hi guys
I'm playing with the debug serial port of my tds 420 scope.
i've found these things:
- Only 3 wires are actually needed ; gnd, rx, tx. Voltage levels are rs232 standard. With only 3 wires connected, hardware flow control won't work, but shouldn't be a problem.
- you can actually give commands to the scope os, and call functions.
- Help command gives the following output:

```
-> help

help                       Print this list
dbgHelp                    Print debugger help info
nfsHelp                    Print nfs help info
netHelp                    Print network help info
spyHelp                    Print task histogrammer help info
timexHelp                  Print execution timer help info
h         [n]              Print (or set) shell history
i         [task]           Summary of tasks' TCBs
ti        task             Complete info on TCB for task
sp        adr,args...      Spawn a task, pri=100, opt=0, stk=7000
taskSpawn name,pri,opt,stk,adr,args... Spawn a task
td        task             Delete a task
ts        task             Suspend a task
tr        task             Resume a task
d         [adr[,nwords]]   Display memory
m         adr              Modify memory
mRegs     [task]           Modify a task's registers interactively
d0-d7,a0-a7,sr,pc  [task]  Display a register of a task
version                    Print VxWorks version info, and boot line
iam       "user"[,"passwd"]  Set user name and passwd
whoami                     Print user name
devs                       List devices
cd        "path"           Set current working path
pwd                        Print working path
ls        ["path"]         List contents of directory
rename    "old","new"      Change name of file
copy      ["in"][,"out"]   Copy in file to out file (0 = std in/out)
ld        [syms[,noAbort]] Load std in into memory
                             (syms = add symbols to table:
                              -1 = none, 0 = globals, 1 = all)
lkup      ["substr"]       List symbols in system symbol table
lkAddr    adr              List symbol table entries near address
checkStack  [task]         List task stack sizes and usage
printErrno  value          Print the name of a status value
periodi   secs,adr,args... Spawn task to call function periodically
repeat    n,adr,args...    Spawn task to call function n times (0=forever)
diskinit  "device"         Format and initialize RT-11 device
squeeze   "device"         Squeeze free space on RT-11 device
```

NOTE: arguments specifying 'task' can be either task id or "name"

- you can use libManagerWordAtPut call to "set" nvram values (to be tested!)
- you can use libManagerWordAt to read the actual nvran value.

Seems actually possible to enable options directly from the debug port, without any expensive gpib card.
With the following commands, taken from other threads here in tek.com/forum, should be possible to enable options

```
libManagerWordAtPut(0x50006, 1)          <- Enable option 1M
libManagerWordAtPut(0x50007, 1)          <- Enable option 05
libManagerWordAtPut(0x50008, 1)          <- Enable option 13
libManagerWordAtPut(0x50009, 1)          <- Enable option 2F
libManagerWordAtPut(0x5000a, 1)          <- Enable option 1F
libManagerWordAtPut(0x5000c, 1)          <- Enable option 2C
libManagerWordAtPut(0x5000d, 1)          <- Enable option 3C
libManagerWordAtPut(0x5000e, 1)          <- Enable option 4C
libManagerWordAtPut(0x5000f, 1)          <- Enable option 2M
```
With the following commands, we can read the actual flag statuses

```
libManagerWordAt 0x50006
libManagerWordAt 0x50007
libManagerWordAt 0x50008
libManagerWordAt 0x50009
libManagerWordAt 0x5000a
libManagerWordAt 0x5000c
libManagerWordAt 0x5000e
libManagerWordAt 0x5000f
```

I've tried to enable all flags on my tds420, but options aren't activate, altough i can clearly read back values, even after power cycling the scope.
My oscilloscope has a very old fw version (1.3) that doesn't even have rolling mode; i suspect that this particular fw version doesn't have these options implemented.

does anyone have a firmware update ?
Feel free to test these command, please use with care!  :D
Top
mirco
Posts: 21
Joined: November 12th, 2014, 9:00 am
Re: TDS 420 Debug Serial Port
Quote
Post  by mirco » November 22nd, 2014, 4:44 pm

Found other useful commands:

```
scopeErrorLogDumpToConsole
```
will write to console the content of error log
```
scopeErrorLogClear
```
will clear the error log!
These commands works on my tds420

Top
vaualbus
Posts: 44
Joined: May 5th, 2013, 2:44 pm
Re: TDS 420 Debug Serial Port
Quote
Post  by vaualbus » November 23rd, 2014, 11:36 am

What software have tou used for the terminal?
Top
mirco
Posts: 21
Joined: November 12th, 2014, 9:00 am
Re: TDS 420 Debug Serial Port
Quote
Post  by mirco » November 23rd, 2014, 11:43 am

I've used a small program called "Putty"
You can find it here (click on 1st putty.exe link) http://www.chiark.greenend.org.uk/~sgta ... nload.html
After opening the program, select "Serial" under Connection type and, if needed, adjust com port number; the default is COM1.
Now, on left menu tree, click on last item labeled as "Serial".
Set the following params
Serial line to connect to: COM1 (change if needed)
Speed (baud): 9600
Data Bits: 8
Stop Bits: 1
Parity: None
Flow Control: None

Now click Open to get connected.
Power up the scope and you'll get a lot of debug info regarding autotests;
once the scope is booted, just to make a test, try to send the letter "i" followed by return key; some other debug information will be printed.
At this point you're ready to use commands.
Top
kc4sw
Posts: 21
Joined: December 11th, 2012, 11:25 am
Re: TDS 420 Debug Serial Port
Quote
Post  by kc4sw » November 25th, 2014, 9:44 am

This is a bit off to the side on the thread, but. Have you tried any of this on the TDS540 series?

thanks!
steve 
s dot hanselman at datagatesystems dot com
Stephen Hanselman
Datagate Systems, LLC
+1.775.882.5117
Top
mirco
Posts: 21
Joined: November 12th, 2014, 9:00 am
Re: TDS 420 Debug Serial Port
Quote
Post  by mirco » November 25th, 2014, 12:09 pm

No, i've not tried, but i'm confident it's working.
Here is another thread where you can see that some of these commands works on TDS7xx
http://www1.tek.com/forum/viewtopic.php ... Put#p10875
Top
string13
Posts: 6
Joined: January 16th, 2015, 6:46 am
Re: TDS 420 Debug Serial Port
Quote
Post  by string13 » January 25th, 2015, 7:46 pm

Hi micro,

I have a pair of TDS 460's that I am playing with. Can you help with the connection of the serial debug port? Or maybe someone else got this to work?

On the ten-pin header closest to the rear of the scope (as these have two ports), looking at the pins, we see this (hopefully my ascii art works) 
_________
| 1 2 3 4 5 |
| 6 7 8 9 10|
///////////////////////////////// (board) 

I found that 1 and 7 are tied together, 4,5,6 don't seem to be connected, and 2 is connected to pin 3 (Tx) of the MC145406, 3 is connected to pin 2 (Rx), 8 is connected to pin 5 (Tx), and I couldn't find what 9 was connected to. 10 is signal ground. 

After some experimenting, I can read the diagnostics just fine connecting my PC serial port Rx to pin8, and signal ground pin 10. I couldn't send anything to the scope however. I'm guessing the two Rx and Tx on the scope header is for the two data lines and two flow control lines - not required, it seems. 

So I don't know if I have a setting wrong on my terminal to transmit (do you need to send a CR and / or LF after command) or maybe my probing isn't correct! Which pin is the Rx on the scope header block?

Thanks so much I am learning so much from these threads...
Top
mirco
Posts: 21
Joined: November 12th, 2014, 9:00 am
Re: TDS 420 Debug Serial Port
Quote
Post  by mirco » January 28th, 2015, 12:52 pm

based on your pin number, you should connect pin 7 with tx (pin 3 on db9) of your serial port.
i suggest the following test:
with oscilloscope disconnected, short tx with rx on your serial port (pin 3 and 2).
Use Putty and, under Serial options, set None as flow control.
Now if you write something, you'll see characters echoed back, so you'll be sure that flow control has been entirely disabled.
Then you can proceed with oscilloscope.
Here are two images representing both end of my rs232 cable
http://it.tinypic.com/r/1414hdx/8
http://it.tinypic.com/r/287ohts/8

Sorry for my bad english :)
Top
string13
Posts: 6
Joined: January 16th, 2015, 6:46 am
Re: TDS 420 Debug Serial Port
Quote
Post  by string13 » February 2nd, 2015, 4:19 pm

Thanks mirco, that did the trick!

Not very many instructions were recognized by the TDS 460 scope, interestingly (returned "undefined symbol" for most of them). For example "HELP" didn't work, but the "dump error log" and "clear error log" sure did! That's worth building this simple interface for! 

And the info during boot would probably be useful if a TDS has boot issues or doesn't pass SPC.

Anyone have a hint what the other debug port is for???? Why two of them? hmmm......

Well, back to fixing a dead primary on one of the power supplies. It was blowing fuses, shorted main transistor, R10 (470R) exploded. Seemed to also take out the FET, but the rest looks OK. Some people also reported that R11 (1K0) also blew up. I will replace those with some flame-proof fusable ones to eliminate future fireworks. 

Hopefully the driver transfo is still OK (and the crazy custom hybrid PWM unit). The driver windings have continuity, but I removed it to try the "ring test" on it and some windings (especially driving the base of the main transistor) looked a little weak. Hopefully it's not a shorted blob under the tape! Some substitute parts are on order, will post results if my parts choices work! 

After that, more SMT cap replacement madness!

Rock on!
Top
dukeluca86
Posts: 6
Joined: June 23rd, 2014, 9:40 am
Re: TDS 420 Debug Serial Port
Quote
Post  by dukeluca86 » June 16th, 2015, 4:09 am

Hello, i'm reading this thread just now, i have a tds520d, not a 400 series one but they have lots of common features, ie the possibility to enable/disable options from console port, so i was wondering if anyone here know the way to backup the nvram content via console port.
I have read about this possibility here and on eev but without the commands to do it, so if you know please tell me.
Top
Drifter
Posts: 1
Joined: February 11th, 2016, 2:57 am
Re: TDS 420 Debug Serial Port
Quote
Post  by Drifter » February 12th, 2016, 3:41 am

dukeluca86 wrote:
Hello, i'm reading this thread just now, i have a tds520d, not a 400 series one but they have lots of common features, ie the possibility to enable/disable options from console port, so i was wondering if anyone here know the way to backup the nvram content via console port.
I have read about this possibility here and on eev but without the commands to do it, so if you know please tell me.
I definitely think this is possible as I've seen people talking about it. Anyone have any tutorials or a guide on how to backup nvram content from the console port?
