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


class TankSim:


	# pin_map[channel] = gpio_index

	#def __init__(self, addr, is_output, pin_map):
	def __init__(self):
		
		self.low_thresh = 10.0
		self.high_thresh = 85.0
		self.high_high_thresh = 95.0
		
		self.simio = SimIO()
		self.last_update = 0
		self.time_scale = 1.0
		
		
		self.pump = AcceleratingActuatorSim(10.0, 2.0, 1.0)
		self.valve = AcceleratingActuatorSim(100.0, 50.0, 50.0)
		
		
		
		self.level_sp = 30.0
		self.inflow_sp = 50.0

		
		# 100 - full,  0 - empty
		# I:0.4
		self.water_level = 0.0
		
		# I:0.5  100-max 0-none
		self.inflow_rate = 0.0
		
		
		self.overflow = False
		
		
		# O:0/0
		self.pump_on = 0
		# O:0/1
		self.valve_open = 0

		# O:0/2
		self.low_ind = 0
		# O:0/3
		self.high_ind = 0
		# O:0/4
		self.high_high_ind = 0
		
		
		
		# I:0/0
		self.low_float = 0
		# I:0/1
		self.high_float = 1
		# I:0/2
		self.high_high_float = 0
		
		# I:0/3
		self.level_sp_0 = 0
		# I:0/4
		self.level_sp_1 = 0
		
		# I:0/5
		self.inflow_sp_0 = 0
		# I:0/6
		self.inflow_sp_1 = 0
		
		
		
		
		
		# Project Select for Demo:
		# I:0/7
		self.proj0 = 0
		# I:0/8
		self.proj1 = 1
		# I:0/9
		self.proj2 = 0
		
		
	
	
	
	def close(self):
		self.simio.close()
		
		
	
	def update_io(self):
	
		vals = [0] * 10
		vals[0] = int(self.low_float)
		vals[1] = int(self.high_float)
		vals[2] = int(self.high_high_float)
		
		vals[3] = int(self.level_sp_0)
		vals[4] = int(self.level_sp_1)
		
		vals[5] = int(self.inflow_sp_0)
		vals[6] = int(self.inflow_sp_1)
		
		vals[7] = self.proj0
		vals[8] = self.proj1
		vals[9] = self.proj2
		
		
		self.simio.write_dig_ins(vals)
	
	
		vals = [int(self.water_level * 40.95), int(self.inflow_rate * 409.5)]
		
		self.simio.write_ang_ins(vals)
		
		
		
	def update(self):
	
		if self.last_update == 0:
			self.last_update = time.time()
	
		relay_vals = self.simio.read_relay_outs()
			
		self.pump_on = relay_vals[0]
		self.valve_open = relay_vals[1]
		# self.pump_on = True
		# self.valve_open = True
		

		self.low_ind = relay_vals[2]
		self.high_ind = relay_vals[3]
		self.high_high_ind = relay_vals[4]
		

		# Vals range 0-10
		# Setpoints range 0-100
		ang_vals = self.simio.read_ang_outs()
		self.pump.setpoint = ang_vals[0] * 10.0
		self.valve.setpoint = ang_vals[1] * 10.0
		
		
		t = time.time()
		time_dif = self.time_scale * (t - self.last_update)
		self.last_update = t
		
		
		self.pump.enabled = self.pump_on
		self.pump.update(time_dif)
		
		self.valve.enabled = self.valve_open
		self.valve.update(time_dif)
		
		
		# Scale to 0-100 to display
		self.inflow_rate = self.pump.position

		self.water_level += time_dif * self.pump.position
		
		
		# 100 - closed,  0 - open
		self.water_level -= time_dif * (100.0 - self.valve.position) * 10.0 / 100.0
			
		
		self.overflow = self.water_level > 100
		
		if self.water_level > 100:
			self.water_level = 100.0
			
		if self.water_level < 0:
			self.water_level = 0.0
			
		
		self.low_float = int(self.water_level) > self.low_thresh
		self.high_float = int(self.water_level) > self.high_thresh
		self.high_high_float = int(self.water_level) > self.high_high_thresh
		
		
		self.level_sp_0 = self.level_sp > 50 
		self.level_sp_1 = self.level_sp % 40 == 0
		
		# Vals: 0, 3, 7, 10
		#print(self.inflow_sp)
		self.inflow_sp_0 = self.inflow_sp == 70 or self.inflow_sp == 100
		self.inflow_sp_1 = self.inflow_sp == 30 or self.inflow_sp == 100
		
		
		
		self.update_io()
	
	
	
	
	
		
		