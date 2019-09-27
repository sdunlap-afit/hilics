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



# TODO: ALARM Conditions




class DoorSim:

	#def __init__(self, addr, is_output, pin_map):
	def __init__(self):
		
		self.simio = SimIO()
		self.last_update = 0
		self.time_scale = 1.0
		
		# 10.0 percent per second
		# 5.0 Percent per second per second
		self.motor = AcceleratingActuatorSim(10.0, 10.0, 100.0, allow_reverse = True)
		self.motor.alarm_timeout = 2.0
		
		self.btm_alarm = False
		self.top_alarm = False
		self.motor_alarm = False
		
		self.top_alarm_time = 0
		self.btm_alarm_time = 0
		
				
		# 100 - closed,  0 - open
		self.doorpos = 100
		
		# O:0/0
		self.motor_up = 0
		# O:0/1
		self.motor_down = 0

		# O:0/2
		self.open_ind = 0
		# O:0/3
		self.closed_ind = 0
		# O:0/4
		self.ajar_ind = 0
		
		
		# I:0/0
		self.open_switch = 0
		# I:0/1
		self.closed_switch = 1
		
		# I:0/2
		self.open_btn = 0
		# I:0/3
		self.close_btn = 0
		# I:0/4
		self.stop_btn = 0
	
		# I:0/5
		self.prox_switch = 0
		
		# I:0/6
		self.impact_switch = 0
		
		# How long the car has been shown
		self.car_time = 0.0
		
		# Amount of time the car stays present
		self.car_event_time = 10.0
	
	
		# Project Select for Demo:
		# I:0/7
		self.proj0 = 0
		# I:0/8
		self.proj1 = 1
		# I:0/9
		self.proj2 = 1
		
		
	
	
	def close(self):
		self.simio.close()
		
	
	
	def update_io(self):
		vals = [0] * 10
		vals[0] = int(self.open_switch)
		vals[1] = int(self.closed_switch)
		vals[2] = int(self.open_btn)
		vals[3] = int(self.close_btn)
		vals[4] = int(self.stop_btn)
		vals[5] = int(self.prox_switch)
		vals[6] = int(self.impact_switch)
		
		vals[7] = self.proj0
		vals[8] = self.proj1
		vals[9] = self.proj2
		
		self.simio.write_dig_ins(vals)
	
		
	
	
	# Time out alarm after 5 seconds
	def update_alarms(self, t):
		
		if self.btm_alarm and (t - self.btm_alarm_time) > 2.0:
			self.btm_alarm = False
			
		if self.top_alarm and (t - self.top_alarm_time) > 2.0:
			self.top_alarm = False
			
			
	
	def begin_car(self, e):
		self.prox_switch = 1
		self.car_time = 0.0
		
		
		
	def update(self):
	
		if self.last_update == 0:
			self.last_update = time.time()
	
		vals = self.simio.read_relay_outs()
			
		self.motor_up = vals[0]
		self.motor_down = vals[1]

		self.open_ind = vals[2]
		self.closed_ind = vals[3]
		self.ajar_ind = vals[4]
		
		t = time.time()
		time_dif = self.time_scale * (t - self.last_update)
		self.last_update = t
		
		self.update_alarms(t)
		
		
		if self.prox_switch:
			self.car_time += time_dif
			if self.car_time > self.car_event_time:
				self.prox_switch = 0
				self.car_time = 0.0
		
		
		
		self.motor.enabled = not self.motor_down == self.motor_up
		# Motor rate will be negative when motor is in up (i.e., reverse)
		self.motor.reverse = self.motor_up
		self.motor.update(time_dif)
		
		
		self.motor_alarm = self.motor.alarm or (self.motor_down and self.motor_up)
		
		# 100 - closed,  0 - open
		self.doorpos += time_dif * self.motor.position
			
		
		if self.doorpos > 100.0:
			self.doorpos = 100.0
			self.motor.position = 0.0
			
			if abs(self.motor.position) > 2.0:
				#self.btm_alarm = True
				self.btm_alarm_time = t
			
		if self.doorpos < 0.0:
			self.motor.position = 0.0
			self.doorpos = 0.0
			
			if abs(self.motor.position) > 2.0:
				#self.top_alarm = True
				self.top_alarm_time = t
			
		
		self.impact_switch = self.prox_switch and self.doorpos > 45
		
		
		self.open_switch = int(self.doorpos) > 1.0
		self.closed_switch = int(self.doorpos) > 99.0
		
		
		if (not self.open_switch) and (not self.motor_up):
			self.open_btn = 0
			
		if self.closed_switch and (not self.motor_down):
			self.close_btn = 0
		
		self.update_io()
	
	
	
	
	
		
		