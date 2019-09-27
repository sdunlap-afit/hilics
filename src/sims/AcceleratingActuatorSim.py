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


import math


##### Description
#
# This class provides a simulation for an actuator that takes into account
# Position, Velocity and Acceleration.
#
# These values can represent any actuator
#
# Pump Example:
# 	RPM 	- current "position"
#	RPM/s	- current "velocity"
#	RPM/s/s	- current "acceleration"
# 
# This level of simulation is necessary for processes that use PID control.
# 
# Without this realism, the process is too "ideal" and the PID
# control works perfectly without any tuning.
#

class AcceleratingActuatorSim:



	# All values should be positive
	def __init__(self, max_p, max_v, max_a, allow_reverse=False):
		
		
		# Current position
		self.position = 0.0
		self.velocity = 0.0
		self.acceleration = 0.0
		
		
		# maximum position
		self.max_p = abs(max_p)

		# DeltaP/s
		self.max_v = abs(max_v)

		# DeltaV/s
		self.max_a = abs(max_a)
		
		self.allow_reverse = allow_reverse
		self.reverse = False
		
		# Percent of max flow rate
		# setpoint should always be positive
		self.setpoint = 100.0
		
		self.enabled = False
	
		self.alarm = False
		self.alarm_time = 0.0
		self.alarm_timeout = 2.0
		
		# Should be positive
		self.reverse_limit = 1.0
	
	
	
	def avg(self, nums):
		return sum(nums)/len(nums)
	
	
	
	def alarm_reset(self, time_dif):
		if self.alarm:
			self.alarm_time += time_dif
			
			if self.alarm_time > self.alarm_timeout:
				self.alarm = False
				self.alarm_time = 0.0
	
	
	
	def check_rev_alarm(self, target_p):
		if self.reverse_limit < 0.0:
			self.reverse_limit = 0.0 - self.reverse_limit
		
		if target_p > self.reverse_limit and self.position < -self.reverse_limit:
			self.alarm = True
			
		if target_p < -self.reverse_limit and self.position > self.reverse_limit:
			self.alarm = True
	
	
	
	
	def clamp(self, n, minn, maxn):
		return max(min(maxn, n), minn)
	
	
	
	
	def update(self, time_dif):
		
		self.alarm_reset(time_dif)
		
		if self.setpoint < 0.0:
			self.setpoint = 0.0 - self.setpoint
		
		
		
		# Target position based on setpoint
		target_p = self.setpoint * self.max_p / 100.0
		
		
		# Target is 0 if not enabled
		if not self.enabled:
			target_p = 0.0
			
		elif self.allow_reverse and self.reverse:
			# Negative target if in reverse and bidirectional
			target_p = 0.0 - target_p
		
			
		# Alarm stuff
		self.check_rev_alarm(target_p)
		
	
		
		
		# difference between target rate and current position
		# can be positive or negative
		delta_p = target_p - self.position
		
		dir = 1
		if delta_p < 0.0:
			dir = -1
			delta_p = abs(delta_p)
			
		
		# The delta_p we'll achieve if we start stopping now
		# dP = (Vt^2 - Vc^2) / 2A
		# Always positive
		min_delta_p = (self.velocity * self.velocity) / (2 * self.max_a)
				
		
		### Determine Target Velocity ###
		
		if delta_p > min_delta_p:

			target_v = dir * self.max_v
			#self.acceleration = dir * self.max_a
		
		else:
			# Limit velocity to prevent overshoot
			target_v = 0.0
			#self.acceleration = dir * (0.0 - self.max_a)
			
		
		
		
		### Determine Velocity ###
		delta_v = target_v - self.velocity
		
		if abs(delta_v) > abs(self.max_a * time_dif):
			delta_v = (delta_v/abs(delta_v)) * self.max_a * time_dif
		
		
		self.velocity += delta_v
		
		self.velocity = self.clamp(self.velocity, 0.0-self.max_v, self.max_v)
		
		
		### Determine Position ###
		
		self.position += self.velocity * time_dif
		
		
		if not self.allow_reverse:
			self.position = self.clamp(self.position, 0.0, self.max_p)
		else:
			self.position = self.clamp(self.position, -self.max_p, self.max_p)
	
	






























