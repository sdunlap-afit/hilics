#!/usr/bin/env python3
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

try:
	import Tkinter as tk
	from Tkinter import ttk
	from Tkinter.font import Font
except ImportError:
	import tkinter as tk
	from tkinter import ttk
	from tkinter.font import Font

import math

class Dial():
	
	
	def __init__(self, master, sx, sy, diameter=100, minval=0.0, maxval=10.0, step=1.0, text=None, text_font=("Helvetica", 10), bg=None, fg=None, dead_angle=90.0):
		self.master = master
		self.bg = bg
		self.fg = fg
		self.diameter = diameter
		self.radius = diameter / 2
		self.minval = minval
		self.maxval = maxval
		self.step = step
		self.dead_angle = dead_angle
	
		self.canvas = master
		self.sx = sx
		self.sy = sy
		
		self.canvas.create_oval(self.sx, self.sy, self.sx + diameter, self.sy + diameter, outline=self.fg, fill=self.bg)
		
		
		if not text is None:
			self.canvas.create_text(self.sx + self.radius, self.sy + diameter*7/8, text=text, font=text_font, fill=self.fg, anchor='c')
		
		
		self.create_ticks()
		
		
		self.ind_line = self.canvas.create_line(self.sx + self.radius, self.sy + self.radius,  self.sx + 5, self.sy + self.radius, fill=self.fg, width=2)
		self.update(0.0)
		
		
		
	def create_ticks(self):
		val = self.minval

		min_angle = 90.0 + (self.dead_angle / 2.0)
		max_angle = 360 + 90.0 - (self.dead_angle / 2.0)
		
		while val <= self.maxval:
			
			angle = (((val - self.minval) * (max_angle - min_angle)) / (self.maxval - self.minval)) + min_angle
			rad = math.pi * angle / 180.0
			
			r = self.radius
			sx = self.radius + int(r * math.cos(rad))
			sy = self.radius + int(r * math.sin(rad))
			
			r = self.radius - 3
			ex = self.radius + int(r * math.cos(rad))
			ey = self.radius + int(r * math.sin(rad))
			
			self.canvas.create_line(self.sx + sx, self.sy + sy, self.sx + ex, self.sy + ey, fill=self.fg, width=2)
			
			r = self.radius - 12
			ex = self.radius + int(r * math.cos(rad))
			ey = self.radius + int(r * math.sin(rad))
			
			self.canvas.create_text(self.sx + ex, self.sy + ey, text='{}'.format(int(val)), fill=self.fg, font=("Helvetica", 5), anchor='c')
			
			val += self.step
			
	
	def update(self, value):
		
		# 90° -> Down
		# 180° -> Left
		# 270° -> Up
		# 360° -> Right
		
		if value > self.maxval:
			value = self.maxval
		
		if value < self.minval:
			value = self.minval
		
		
		
		min_angle = 90.0 + (self.dead_angle / 2.0)
		max_angle = 360 + 90.0 - (self.dead_angle / 2.0)
		
		angle = (((value - self.minval) * (max_angle - min_angle)) / (self.maxval - self.minval)) + min_angle
		
		rad = math.pi * angle / 180.0
		
		r = self.radius - 5
		ex = self.radius + int(r * math.cos(rad))
		ey = self.radius + int(r * math.sin(rad))
		self.canvas.coords(self.ind_line, self.sx + self.radius, self.sy + self.radius, self.sx + ex, self.sy + ey)
	
	

		
		
		
		