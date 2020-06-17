
**This is my scrapbook related to my Tektronix TDS 420A oscilloscope: drafts, some code, experiments. Don't expect things in the repo to be well organized or usable in any way. Eventually, some of the info here may end up in some blog post.**

# GPIB

## PyVisa

pip3 install gpib_ctypes


* Tek 420A Programmers Manual: http://w140.com/tekwiki/images/c/cd/070-8709-07.pdf

Fetching waveform:
    * See page 2-32 of programmers manual
    * `ACQ?`: Get acquistion parameters

```
RUNST;0;SAM;10;16;1
```
    * `ACQ:STATE RUN` : start acquisition
    * `ACQ:STATE STOP` : stop acquisition
    * `DATA:SOURCE CH1` : select data channel to fetch
    * `DATA:SOURCE CH1,CH2,CH3,CH4` : fetch multiple channels at once
    * `WFMPRE?` : waveform preamble information of all data:source channels
    * `CURV?` : waveform data
    * `WAVF?`: waveform preamble and waveform data together


Single acquistion:

    * `ACQ:STOPA SEQ`
    * `ACQ:REPE 1`
    * `ACQ:STATE ON`

Continuous acquistion:

    * `ACQ:STOPA RUNST`
    * `ACQ:STATE ON`



## USB permissions

(doesn't work...)

sudo vi /etc/udev/rules.d/72-linux_gpib_ni_usb.rules

SUBSYSTEMS=="usb", ACTION=="add", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="3923", ATTR{idProduct}=="709b", MODE="666", GROUP="tom", SYMLINK+="usb_gpib"
SUBSYSTEMS=="usb", ACTION=="add", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="3923", ATTR{idProduct}=="709b", RUN+="/usr/local/sbin/gpib_config"
KERNEL=="gpib[0-9]*", ACTION=="add", MODE="666", GROUP="tom"



```
sudo udevadm control -R
sudo udevadm monitor -e
udevadm info /dev/gpib0
```

In udev rule:
```
TAG+="test_gpib0"
```
This tag will show up in udevadm monitor



