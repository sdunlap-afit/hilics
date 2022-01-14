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

import time
from random import random

from sims.SimIO import SimIO
from sims.AcceleratingActuatorSim import AcceleratingActuatorSim
from sims.MicroLogixComm import MicroLogixComm


##### IO List #####
##
## Analog Inputs (2 max)
##		Temperature
##		Humidity
##
## Analog Outputs (4 max)
## 		Damper - Controls temperature
##		Pump(?) - Controls humidity
## 		
## Digital Inputs (10 max)
##		Door open/closed
##		Locked/Unlocked
##		Lights on/off
## 		Motion (for alarm and/or unlocking door from inside - fire code)
##		Fire
##		Additional overheat sensor??
##		
## Digital outputs (6 max)
##		Lights
##		Door unlock
##		Intrusion alarm
##		Fire alarm
##		Fire supression (gas?)
## 		
##
## NOTE: Additional "network" sensors can be provided - the RPI can send the value to the PLC via Ethernet
##
##


### Class for calculating the current temperature and heat dissapated
### by a temperature zone
###
class Zone:

	def __init__(self, wall_area, cubic_feet):
		# Start at 70°F
		self.temp = 65.0 + (random() * 10.0)
		self.wall_area = wall_area
		self.cubic_feet = cubic_feet


	def update(self, delta_time, outside_temp):
		# http://www.sensiblehouse.org/nrg_heatloss.htm
		#	Simplified heat loss
		#		BTU/hr = Area * U (insulation const) * delta_temp
		# https://www.ferrellgas.com/tank-talk/blog-articles/how-many-btus-you-need-to-heat-your-home-shop-garage-and-more/
		# BTU/hr required to change temperature 
		# 	BTU/hr = (t_outside - t_inside) x (cubic feet) x .133 

		self.temp = (self.temp + random() * 5.0 * delta_time)
		if self.temp > 120.0:
			self.temp = 70.0


### Class for calculating the status and amount of heat generated by each server
###
class Server:

	def __init__(self):
		
		# The status will determine the percentage of heat
		# generated by the server
		self.RUNNING = 1.0
		self.THROTTLED = 0.5
		self.SHUTDOWN = 0.0
		
		# 0 - 1 °F/min
		self.deg_per_minute = random()

		self.status = self.RUNNING
		self.thresh = 90.0 + random() * 20.0
	

	def update(self, temp):
		if temp < self.thresh:
			self.status = self.RUNNING
		elif temp < self.thresh + 10:
			self.status = self.THROTTLED
		else:
			self.status = self.SHUTDOWN

	def get_temp_out(self, delta_t):
		self.deg_per_minute * delta_t * self.status




class ServerSim:


	# pin_map[channel] = gpio_index

	#def __init__(self, addr, is_output, pin_map):
	def __init__(self):
		
		# update values 10x per second
		self.mlupdateperiod = 0.1

		self.mlcomm = MicroLogixComm()
		self.mlcomm.connect()
		self.mlcomm.test_connection()

		

		self.num_servers = 14
		self.servers = []

		for i in range(self.num_servers):
			self.servers.append(Server())

		# Assume a square 100' by 100' building with 10' ceiling
		# volume - 100,000 cubic ft
		# wall surface area = 6000 sq ft  (4 walls + ceiling + floor)
		self.building = Zone(6000.0, 100000.0)

		self.server_room = Zone(600.0, 1000.0)

		self.simio = SimIO()
		self.last_update = 0
		self.time_scale = 1.0
		
		# I:0/0
		self.z0_damper = AcceleratingActuatorSim(100.0, 50.0, 50.0)

		# I:0/1
		self.z0_reheat = AcceleratingActuatorSim(10.0, 2.0, 1.0)
		
		# I:0/0
		self.z0_temp = 0.0
		# I:0/1
		self.z0_humidity = 0.0

		# O:0/0
		self.relay_out_0 = 0
		# O:0/1
		self.relay_out_1 = 0
		# O:0/2
		self.relay_out_2 = 0
		# O:0/3
		self.relay_out_3 = 0
		# O:0/4
		self.relay_out_4 = 0
		# O:0/5
		self.relay_out_5 = 0
		
		
		# I:0/0
		self.dig_in_0 = 0
		# I:0/1
		self.dig_in_1 = 0
		# I:0/2
		self.dig_in_2 = 0
		# I:0/3
		self.dig_in_3 = 0
		# I:0/4
		self.dig_in_4 = 0
		# I:0/5
		self.dig_in_5 = 0
		# I:0/6
		self.dig_in_6 = 0
		
		
		# Project Select for Demo:
		# I:0/7 - I:0/9
		self.proj0 = 0
		self.proj1 = 0
		self.proj2 = 1
		
		
		# I:0.4
		self.analog_in_0 = 0.0
		# I:0.5
		self.analog_in_1 = 0.0


		
	
	
	
	def close(self):
		self.simio.close()



	def update_plc_inputs(self):
	
		vals = [0] * 10
		vals[0] = int(self.dig_in_0)
		vals[1] = int(self.dig_in_1)
		vals[2] = int(self.dig_in_2)
		vals[3] = int(self.dig_in_3)
		vals[4] = int(self.dig_in_4)
		vals[5] = int(self.dig_in_5)
		vals[6] = int(self.dig_in_6)
		
		vals[7] = self.proj0
		vals[8] = self.proj1
		vals[9] = self.proj2
		
		self.simio.write_dig_ins(vals)
	
	
		vals = [self.analog_in_0, self.analog_in_1]
		
		self.simio.write_ang_ins(vals)
		
		
		
	def update(self):
	
		##### Init Simulation Timer #####
		
		if self.last_update == 0:
			self.last_update = time.time()
	
	
		##### Read PLC Analog Outputs #####

		analog_vals = self.simio.read_ang_outs()

		# 0 - 100%
		self.z0_damper.setpoint = analog_vals[0] * 10.0
		self.z0_reheat.setpoint = analog_vals[1] * 10.0
	
		##### Read PLC Relay Outputs #####
		
		relay_vals = self.simio.read_relay_outs()
			
		self.relay_out_0 = relay_vals[0]
		self.relay_out_1 = relay_vals[1]
		self.relay_out_2 = relay_vals[2]
		self.relay_out_3 = relay_vals[3]
		self.relay_out_4 = relay_vals[4]
		self.relay_out_5 = relay_vals[5]
		
		
		
		##### Calculate Time Since Last Update (Seconds) #####
		
		t = time.time()
		delta_t = self.time_scale * (t - self.last_update)
		self.last_update = t
		
		
		
		##### Simulation Logic and Calculations #####
		
		# Put code here
		
		# delta_t is the amount of time that has elapsed since the last update
		# use this value to determine how much the process has changed.
		
		self.building.update(delta_t, 100.0)
		
		self.server_room.update(delta_t, self.building.temp)
		
		for server in self.servers:
			server.update(self.server_room.temp)


		##### Write PLC Inputs #####
		
		self.update_plc_inputs()
	
	
	
	
	
		
		