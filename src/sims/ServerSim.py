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
from sims.SimIO import SimIO
from sims.AcceleratingActuatorSim import AcceleratingActuatorSim


class ServerSim:


	# pin_map[channel] = gpio_index

	#def __init__(self, addr, is_output, pin_map):
	def __init__(self):
		
		self.simio = SimIO()
		self.last_update = 0
		self.time_scale = 1.0
		
		
		# self.pump = AcceleratingActuatorSim(10.0, 2.0)
		
		
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
		self.proj0 = 1
		self.proj1 = 0
		self.proj2 = 0
		
		
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
	
	
		vals = [int(self.analog_in_0 * 40.95), int(self.analog_in_1 * 40.95)]
		
		self.simio.write_ang_ins(vals)
		
		
		
	def update(self):
	
		##### Init Simulation Timer #####
		
		if self.last_update == 0:
			self.last_update = time.time()
	
	
	
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
		time_dif = self.time_scale * (t - self.last_update)
		self.last_update = t
		
		
		
		##### Simulation Logic and Calculations #####
		
		# Put code here
		
		# time_dif is the amount of time that has elapsed since the last update
		# use this value to determine how much the process has changed.
		
		
		
		
		##### Write PLC Inputs #####
		
		self.update_plc_inputs()
	
	
	
	
	
		
		