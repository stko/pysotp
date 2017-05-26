#!/usr/bin/env python

from Can import *
from FordStuff import key_from_seed

def send(request):
	try:
		answer=iso.iso_tp_send_and_receive( 'iso_tp_channel_1', request,100)
		print(": {0} -> {1}".format(request,answer))
	except:
		print(": {0} -> -".format(request))

secret_keys = {
                0x741: "00 11 22 33 44", # 5 bytes
	}


can_start()
#raw = RawCan()
#raw.raw_can_map_channel('my_channel_1')
#raw.raw_can_send('my_channel_1', '01 23 XX 45')
seed=key_from_seed(0x741,"7A 6B 61",1)
print seed
iso = IsoTp()

iso.iso_tp_map_channel('iso_tp_channel_1')
send('22 A1 91')
send('22 A1 91')
send('22 A1 91')
send('10 03')
send('27 01')
send('27 02')
send('27 03')
send('27 04')
send('27 05')
send('27 06')
