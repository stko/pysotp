# Intro

This a modified version of the original pysotp from OTAKeys (https://github.com/OTAkeys/pysotp). While the original software is made to include isotp into the Robottest Framework, this version is more tailored to allow communication with electronic modules inside vehicles as part of the [OOBD](https://oobd.org) tool sets. For that some functions and structures have been modified.

As the work has just begun, this project is work in progress. So also this installation documentation is not fully error free yet.


# Setup
 ## can-isotp Installation

As the can-isotp kernel module seems not to be available as debian package yet, we compile and use the module only locally and do not install it in the system.

1. Download repository

      git clone https://github.com/hartkopp/can-isotp.git

2. Build ISO-TP kernel module

   Ensure dependencies are installed.  For Debian (or Ubuntu):

      sudo apt-get install build-essential linux-headers-$(uname -r)

   To build:

On Ubuntu 16.04, you might need to tweak the KERNEL_VERSION directive in isotp.c:1112 (just check the error message, in case)

make

   To install (optional):

      sudo make modules_install


3. When the PF_CAN core module is loaded ('modprobe can') the ISO-TP module
   can be loaded into the kernel with

       insmod ./net/can/can-isotp.ko

   When the can-isotp.ko module has been installed into the Linux Kernels
   modules directory (e.g. with 'make modules_install') the module should
   load automatically when opening a CAN_ISOTP socket.



## Pysotp
### A Python library for raw CAN and ISO-TP over SocketCAN

Originally this library was used as a CAN library for robot framework, but it can also be used as a general ISO-TP and raw CAN library for Python.

Usage:

On Ubuntu 16.04, if you have not installed the can-isotp source file, you'll need to change the `#include "linux/can/isotp.h"` to your actual can-isotp source directory  and the `int` to `long` type declarations  (just check the error messages, in case)

add also ` -fpic` to the compiler `CFLAGS` to clear the linker error



```
cd can_wrap_src
make
cd ..
./example.py
```



Set the CAN interface up:
```
$ ip link set can0 up
```

The accompanied udev rule is specific for PCAN-USB CAN interfaces, but can easily be modified for different CAN interfaces.

Copy the udev rule and corresponding script to the right directories:
```
$ cp 90-can-interface.rules /etc/udev/rules.d/
$ cp setup_can_iface.sh /usr/local/bin/
```

Now setup_can_iface.sh script is run by udev when a can interface is plugged in. This script makes sure the correct drivers are loaded and the interface is set to up.

CAVEAT: When a new kernel version is installed, you might have to copy the the can-isotp.ko kernel module again to the modules directory.


## FordStuff
**DISCLAIMER: The Use of the Ford Security Access library might violate laws or regulations in some countries. Install and use that library only when being aware about any potential effects. For further details see also LICENCE**

The FordStuff library is the result of some reverse engineering activities of american scientists. It allows to activate advanced functions on some Ford electronic modules. In case of questions please contact the authors directly, we do not provide any support or further details on that.

By following the instruction about how to install you agree to the a.m. disclaimer and the LICENSE terms.

To install the FordStuff library, execute 

     wget https://github.com/Self-Driving-Vehicle/CANBUS-Hack/raw/master/code/ecomcat_api/FordStuff.py