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

from widgets.Rounded_Rect import Rounded_Rect



class Tank():
	
	
	def __init__(self, canvas, x, y, width, height, bg, fg, sp_color, low_color, high_color):
	
		self.canvas = canvas
		self.setpoint = 200.0
		self.tank_ht = 0.0
		
		self.padding = 2
		self.width = width
		self.height = height
		
		self.sx = x
		self.sy = y
		self.ex = x + width
		self.ey = y + height
		self.radius = (height + width) / 16
		
		self.tank_sy = self.sy + self.padding
		self.tank_ey = self.ey - self.padding
		
		self.tank_sx = self.sx + self.padding
		self.tank_ex = self.ex - self.padding + 1
		
		
		self.bg = bg
		self.fg = fg
		
		self.sp_color = sp_color
		self.low_color = low_color
		self.high_color = high_color
		
		self.flt_ind = []
		self.flt_txt = []
		
		self.create_tank()
		
	
	
	
	def create_tank(self):
	
		##########  Tank Frame  ##########
		
		self.tank_rect = Rounded_Rect(self.canvas, self.sx, self.sy, self.ex, self.ey, radius=self.radius, outline=self.bg, fill=self.bg)
		
		#self.bottom_round_rectangle(self.sx+self.padding, self.tank_ey, self.ex-self.padding, self.ey-self.padding, radius=self.radius, outline=self.fg, fill=self.fg)
		
		
		self.setpoint_line = self.canvas.create_line(self.tank_sx, self.sy, self.tank_ex, self.sy, fill=self.sp_color, width=1)
		self.setpoint_label = self.canvas.create_text(self.ex+5, self.sy, anchor='w', text='Setpoint', fill=self.bg)
		
		ht = int(self.tank_ey - self.tank_sy)
		self.water_lines = []
		offset = 0
		for i in range(0, ht):
			
			if i < (self.radius / 4):
				offset = (self.radius / 4) - i
			elif i > ht - (self.radius / 4):
				offset = (self.radius / 4) - (ht-i)
			else:
				offset = 0
				
		
			y = self.tank_ey - i
			x1 = self.tank_sx + offset
			x2 = self.tank_ex - offset
			
			line = self.canvas.create_line(x1, y, x2, y, fill=self.fg, width=1, state='hidden')
			self.water_lines.append(line)
	
	
	
	# Pass in the coords of the tank
	def add_float(self, thresh, radius, txt, font, lbl):
		
		#x = sx - 30
		x = self.ex - radius - 5
		y = self.sy + int((100.0 - thresh) * (self.ey - self.sy) / 100.0)
		r = radius
		
		ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.low_color, fill=self.low_color)
		txt = self.canvas.create_text(x, y, anchor='c', text=txt, fill=self.sp_color, font=font)
		lbl = self.canvas.create_text(x-r-3, y, anchor='e', text=lbl, fill=self.sp_color, font=font)
		
		self.flt_ind.append(ind)
		self.flt_txt.append(txt)
		self.flt_txt.append(lbl)
		
		return ind
		
		
		
		
	def update_float(self, ind, active):
		if active:
			self.canvas.itemconfig(ind, fill=self.high_color, outline=self.high_color)
		else:
			self.canvas.itemconfig(ind, fill=self.low_color, outline=self.low_color)

		
		
		
		
	
	def bottom_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):

		r = radius
		if y2 - r < y1:
			r = r - (y1 - (y2 - r))
	
		points = [x1, y1,
					x1, y1,
					x2, y1,
					x2, y1,
					x2, y2-r,
					x2, y2-r,
					x2, y2,
					x2-radius, y2,
					x2-radius, y2,
					x1+radius, y2,
					x1+radius, y2,
					x1, y2,
					x1, y2-r,
					x1, y2-r]

		return self.canvas.create_polygon(points, kwargs, smooth=True)



	def update(self, ht, tagraise=True):
		
		if not self.tank_ht == ht:
			
			self.tank_ht = ht
			
			lim = int(self.tank_ht * len(self.water_lines) / 100.0)
			
			#if self.water_rect is None:
			#	self.water_rect = self.canvas.create_rectangle(0, 0, 1, 1, outline=self.water_color, fill=self.water_color, state='hidden')

			#sy = self.tank_ey - int(((self.tank_ey - self.tank_sy) * self.tank_ht) / 100.0)
			
			#self.canvas.coords(self.water_rect, self.tank_sx, sy, self.tank_ex, self.tank_ey)
			
			#self.canvas.itemconfig(self.water_rect, state='normal')
			
			for i in range(0, len(self.water_lines)):
				if i < lim:
					self.canvas.itemconfig(self.water_lines[i], state='normal')
				else:
					self.canvas.itemconfig(self.water_lines[i], state='hidden')
					
			
			
			
			
			
			
			if tagraise:

				self.canvas.tag_raise(self.setpoint_line)

				for id in self.flt_ind:
					self.canvas.tag_raise(id)
					
				for id in self.flt_txt:
					self.canvas.tag_raise(id)



				
				
				
	def update_setpoint(self, sp):
		
		if not sp == self.setpoint:
		
			self.setpoint = sp
			
			y = self.tank_sy + int((self.tank_ey - self.tank_sy) * (1.0 - self.setpoint / 100.0))
			
			self.canvas.coords(self.setpoint_line, self.tank_sx, y, self.tank_ex, y)
			
			t = '{}'.format(int(self.setpoint))
			
			self.canvas.coords(self.setpoint_label, self.tank_ex+8, y)
			self.canvas.itemconfig(self.setpoint_label, text=t)





















