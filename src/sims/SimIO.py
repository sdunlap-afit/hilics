#!/usr/bin/env python
#
# IP: HILICS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import spidev
import time
import os
from xml.etree import ElementTree
import RPi.GPIO as GPIO

EXTENDER_CS = 6
DAC_CS = 5
ADC_CS = 27


##### SPI CONSTANTS #####
# Commands
WRITE_CMD = 0x40
READ_CMD = 0x41
ADDR = 0

# for Inputs
GPIOA = 0x12
GPIOB = 0x13

#for Outputs
OLATA = 0x14
OLATB = 0x15

# These registers determine if the GPIO are inputs or outputs
IODIRA = 0x00
IODIRB = 0x01

# These registers set the internal pullup resistors
GPPUA = 0x0C
GPPUB = 0x0D

# These registers invert the logic for the inputs/outputs
IPOLA = 0x02
IPOLB = 0x03

# These are the config registers
IOCONA = 0x0A
IOCONB = 0x0B

# BANK		=	0
# MIRROR	=	0
# SEQOP		=	0
# DISSLW	=	0
# HAEN		=	1  - enable hardware addressing
# ODR		=	0
# INTPOL	=	0
# NA 		=	0
CONFIG = 0b00001000



class SimIO:


	# pin_map[channel] = gpio_index

	#def __init__(self, addr, is_output, pin_map):
	def __init__(self, verbose=False):
		
		self.dig_ins = []
		self.relay_outs = []
		self.ang_ins = []
		self.ang_outs = []
		
		self.verbose = verbose

		self.spidev = spidev.SpiDev()
		self.spidev.open(0, 0)
		self.spidev.max_speed_hz = 115200
		self.spidev.mode = 0b0
		self.spidev.cshigh = False
		self.spidev.lsbfirst = False
		
		
		self.refresh_time = 0.05
		self.last_time_dig = 0
		self.last_time_ang = 0
		
		
		self.setup()

		
		
	def close(self):
		GPIO.cleanup()
		self.spidev.close()
		
		
	
	def gpio_setup(self):
	
		GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
		
		GPIO.setup(EXTENDER_CS, GPIO.OUT)
		GPIO.setup(ADC_CS, GPIO.OUT)
		GPIO.setup(DAC_CS, GPIO.OUT)
		
		GPIO.output(EXTENDER_CS, GPIO.HIGH)
		GPIO.output(ADC_CS, GPIO.HIGH)
		GPIO.output(DAC_CS, GPIO.HIGH)

		
		
	# Setup GPIO extender
	def setup(self):
		
		self.gpio_setup()
	
		
		GPIO.output(EXTENDER_CS, GPIO.LOW)
		cmd = WRITE_CMD
		to_send = [cmd, IOCONA, CONFIG, CONFIG]
		self.spidev.xfer2(to_send)
		GPIO.output(EXTENDER_CS, GPIO.HIGH)
		
		time.sleep(0.01)
		
		GPIO.output(EXTENDER_CS, GPIO.LOW)
		cmd = WRITE_CMD
	
		# 0 - Output, 1 - Input
		to_send = [cmd, IODIRA, 0b00000000, 0b11111100]
		self.spidev.xfer2(to_send)
		GPIO.output(EXTENDER_CS, GPIO.HIGH)
		
		
		self.write_outputs([0] * 10)
		self.write_ang_ins([0, 0])




	def list_to_int(self, vals):
		res = 0
		
		for i in range(0, len(vals)):
			res = res | vals[i] << i
			
		return res



	def int_to_list(self, val):
		res = [0] * 6
		
		for i in range(len(res), 0, -1):
			res[i-1] = val & 1
			val = val >> 1
		
		return res




	def write_outputs(self, outputs):
		GPIO.output(EXTENDER_CS, GPIO.LOW)

		vals = self.list_to_int(outputs)
		#print('Writing:', vals)
		val1 = vals & 0xFF
		val2 = vals >> 8
		
		cmd = WRITE_CMD
		
		to_send = [cmd, OLATA, val1, val2]
		#print('Writing:', to_send)
		self.spidev.xfer2(to_send)

		GPIO.output(EXTENDER_CS, GPIO.HIGH)
		
		
		

	def read_inputs(self):
		GPIO.output(EXTENDER_CS, GPIO.LOW)

		cmd = READ_CMD
	
		# Having the two trailing bytes allows us to read the
		# result while keeping CS active
		to_send = [cmd, GPIOB, 0x00]
		
		res = self.spidev.xfer2(to_send)
		
		#res_list = [0] * 16
		val = res[2] >> 2
		#print('Got:', val)
		res = self.int_to_list(val)

		GPIO.output(EXTENDER_CS, GPIO.HIGH)
		return res


		
	def write_DAC(self, vals):
		
		for i in range(0, 2):
			GPIO.output(DAC_CS, GPIO.LOW)
			v = vals[i]
	
			firstByte = (v >> 8) | 0b00110000
			secondByte = v & 0x0FF

			firstByte = (i << 7) | firstByte

			to_send = [firstByte, secondByte]

			self.spidev.xfer2(to_send)

			GPIO.output(DAC_CS, GPIO.HIGH)
			
	
	
	def read_ADC(self):
		vals = []
		
		for i in range(0, 4):
			
			GPIO.output(ADC_CS, GPIO.LOW)
			cmd = (0b00011000 | i) << 6;
			
			to_send = [cmd >> 8, cmd & 0x0FF, 0]
			
			res = self.spidev.xfer2(to_send)
			GPIO.output(ADC_CS, GPIO.HIGH)
			
			val = ((res[1] & 0b01111) << 8) | res[2]
			val = (float(val) * 10.0) / 4095.0
			
			vals.append(val)

		if self.verbose:
			print ('ADC:', vals)
		return vals

			
			
			


	def write_dig_ins(self, outputs):
		if (not outputs == self.dig_ins) or time.time() - self.last_time_dig > self.refresh_time:
			self.last_time_dig = time.time()
			self.dig_ins = outputs[:]
			self.write_outputs(self.dig_ins)



	def write_ang_ins(self, vals):
		if (not vals == self.ang_ins) or time.time() - self.last_time_ang > self.refresh_time:
			self.last_time_ang = time.time()
			self.ang_ins = vals[:]
			self.write_DAC(self.ang_ins)



	def read_relay_outs(self):

		vals = self.read_inputs()
		
		if not self.relay_outs == vals:
			self.relay_outs = vals
			self.has_changed = True

		return self.relay_outs


		
	def read_ang_outs(self):

		vals = self.read_ADC()
		
		if not self.ang_outs == vals:
			self.ang_outs = vals
			self.has_changed = True

		return self.ang_outs


















