#!/usr/bin/python
# -*- coding: utf-8 -*-

#-----------------for development only: Load the can module from the local subfolder
import os, sys, inspect

# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)


# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"pysotp")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
from Can import *	
#---------------------------	
	
#from pysotp import *
from modules import modules

import time

import binascii




try:
	from FordStuff import key_from_seed
	import FordStuff

except ImportError:
	def key_from_seed(a,b,c): # dummy declaration, in case FordStuff is not installed
		return False
	
	class FordStuff: # dummy declaration, in case FordStuff is not installed
		secret_keys = {
		}

class SampleModule(IsoTp):	
	def send(self,request):
		try:
			answer=self.iso_tp_send_and_receive( request,500)
			print(": {0} -> {1}".format(request,binascii.hexlify(answer)))
			return answer
		except Exception as inst:
			print type(inst)     # the exception instance
			print inst.args      # arguments stored in .args
			print inst           # __str__ allows args to be printed directly		print(": {0} -> -".format(request))
			return bytearray()
		
		
	def accessMode(self, opMode, seclevel):
		# first of all switch into the requested session mode
		udsBuffer=self.send("10 {:02X}".format(opMode))
		if len(udsBuffer)>0:
			if udsBuffer[0]!=0x50:
				return -1
		else:
			return -2
		if seclevel == 0 :
			return 0 # just changed the mode, nothing more to do
		udsBuffer=self.send("27 {:02X}".format(seclevel))
		if len(udsBuffer)>0:
			if udsBuffer[0]==0x67:
				if udsBuffer[1] == seclevel:
					if udsBuffer[ 2 ] == 0  and  udsBuffer[ 3 ] == 0  and  udsBuffer[ 4 ] == 0:
					# access already granted previously..
						return seclevel
					else:
						# to let FordStuff act correcty, we need to put the code to use first into the right place before call the seed calculation
						FordStuff.secret_keys [self.module["tx"]]=self.module["seccodes"][seclevel]
						seed=key_from_seed(self.module["tx"],"{:02X} {:02X} {:02X}".format( udsBuffer[ 2 ] , udsBuffer[ 3 ] , udsBuffer[ 4 ] ),1)
						udsBuffer=self.send("27 {:02X} {:02X} {:02X} {:02X}".format( seclevel + 1 , seed[ 0 ] , seed[ 1 ] , seed[ 2 ] ) )
						if len(udsBuffer)>0:
							if udsBuffer[ 0 ] == 0x67 and udsBuffer[ 1 ] == seclevel + 1 :
								return seclevel
							else:
								return -4
						else:
							return -5
				else:
					return -6
			else:
				print ("Error response: {:02X} {:02X}".format(udsBuffer[0],udsBuffer[2]))
				return -7
		else:
			return -8


	def simplesend(self,prefix,mask, byteseq):
		#self.iso_tp_send_and_receive(prefix+" "+byteseq+" "+mask,500)
		answer=self.send( prefix+" "+mask+" "+byteseq)
		print(": {0} -> {1}".format(request,binascii.hexlify(answer)))
		time.sleep( 0.3 )
		#self.iso_tp_send_and_receive(prefix+" "+mask+" 00 00 00 00",500)


can_isotp_start()
#raw = RawCan()
#raw.raw_can_map_channel('my_channel_1')
#raw.raw_can_send('my_channel_1', '01 23 XX 45')
seed=key_from_seed(0x726,"7A 6B 61",1)
print seed
myModule = SampleModule("can0",modules["BCM"])



udsBuffer=myModule.send('19 00')
udsBuffer=myModule.send('22 71 51')
if len(udsBuffer)>0:
	if myModule.accessMode( 3, 3 )>-1:
		# original command was: send('2F 71 51 03 00 00 00 0F 00 00 00 0F')
		#mask="F0 00 19 0F" # mask for all outputs
		mask="FF FF FF FF" # mask for all outputs
		#mask="00 00 00 00" # mask for all outputs
		'''
			0x 00 00 00 03
			0x 00 00 00 0c
			0x 00 00 01 00
			0x 00 00 18 00
		       (0x 01 80 00 00 ohne Foglamps)
			0x 30 00 00 00
			0x C0 00 00 00
		=	0x F0 00 19 0F
		''' 


		while True:
		  '''
		  prefix="2F 71 51 03" # External Lighting System Output Signal Status (7151)
		  #Low Beam Lamp RH	31
		  #Low Beam Lamp LH	30
		  myModule.simplesend(prefix,mask,"00 00 00 03")
		  #Direction Indicators Right Hand	25
		  #Direction Indicators Left Hand	24
		  myModule.simplesend(prefix,mask,"00 00 00 0C")
		  #High/Main Beam Relay	23
		  myModule.simplesend(prefix,mask,"00 00 01 00")
		  #Left Position Lamp	20
		  #Right Position Lamp	19
		  myModule.simplesend(prefix,mask,"00 00 18 00")
		  #Front fog light relay	8
		  #Rear fog light	7
		  #myModule.simplesend(prefix,mask,"01 80 00 00")
		  #Right Front Side Turn Indicator	3
		  #Left Front Side Turn Indicator	2
		  myModule.simplesend(prefix,mask,"30 00 00 00")
		  #Daytime Running Light supply left	1
		  #Daytime Running Light supply right	0
		  myModule.simplesend(prefix,mask,"C0 00 00 00")
		  '''
		  prefix="2F A4 61 03" # External Lighting System Output Signal Status (A461)
		  myModule.simplesend(prefix,mask,"02 00 00 00")



