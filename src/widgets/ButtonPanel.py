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



class ButtonPanel():
	
	
	def __init__(self, canvas, prefix, labels, values, font, x, y, width, height, bg, fg, default_val=0):
		self.canvas = canvas
		
		self.frame_sx = x
		self.frame_sy = y
		self.frame_ex = x + width
		self.frame_ey = y + height
		self.frame_radius = (height + width) / 16
		
		self.width = width
		self.height = height
		
		
		self.font = font
		
		self.bg = bg
		self.fg = fg
		
		self.values = values
		self.labels = labels
		
		# If two dimensional list, we need to handle columns
		if isinstance(labels[0], list):
			self.num_cols = len(self.labels) 
			self.num_rows = len(self.labels[0])
		else:
			self.num_cols = 1
			self.num_rows = len(self.labels) 
		
		
		
		self.padding = 4
		self.row_height = (height - ((self.num_rows + 2) * self.padding)) / (self.num_rows + 1)
		
		self.col_width = (width - ((1 + self.num_cols) * self.padding)) / self.num_cols
		
		self.val = default_val
		
		self.prefix = prefix

		self.current_text = '{}{}'.format(self.prefix, self.val)
		self.has_changed = True
		
		
		
		self.create_frame()
		self.create_textfield()
		self.create_buttons()
		
		

	def create_frame(self):
		x1 = self.frame_sx
		y1 = self.frame_sy
		x2 = self.frame_ex
		y2 = self.frame_ey
		r = self.frame_radius
		
		self.frame_rect = Rounded_Rect(self.canvas, x1, y1, x2, y2, r, outline=self.fg, fill=self.fg)
		
		

	def create_textfield(self):
		x1 = self.frame_sx + self.padding
		y1 = self.frame_sy + self.padding
		x2 = self.frame_ex - self.padding
		y2 = y1 + self.row_height
		r = self.frame_radius / 2
		
		self.textrect = Rounded_Rect(self.canvas, x1, y1, x2, y2, r, outline=self.bg, fill=self.bg)
		
		cx = x1 + (x2 - x1) / 2
		cy = y1 + (y2 - y1) / 2
		self.text_obj = self.canvas.create_text(cx, cy, anchor='c', text=self.current_text, fill=self.fg, font=self.font)
		
		
		
	def create_buttons(self):
		
		rad = self.frame_radius / 2
		sy = self.frame_sy + self.padding + self.row_height + self.padding
		sx = self.frame_sx + self.padding
		
		for c in range(0, self.num_cols):
		
			for r in range(0, self.num_rows):
				
				x1 = sx + (c * self.col_width) + (c * self.padding)
				x2 = x1 + self.col_width
				
				y1 = sy + (r * self.row_height) + (r * self.padding)
				y2 = y1 + self.row_height
						
				btn = Rounded_Rect(self.canvas, x1, y1, x2, y2, rad, outline=self.bg, fill=self.bg)

				cx = x1 + (x2 - x1) / 2
				cy = y1 + (y2 - y1) / 2
				
				if self.num_cols > 1:
					t = self.labels[r][c]
					v = self.values[r][c]
				else:
					t = self.labels[r]
					v = self.values[r]
					
				txt = self.canvas.create_text(cx, cy, anchor='c', text=t, fill=self.fg, font=self.font)
				
				self.canvas.tag_bind(txt, '<Button-1>', lambda e, v=v: self.click(val=v))
				self.canvas.tag_bind(btn.id, '<Button-1>', lambda e, v=v: self.click(val=v))
			
			
			
	def click(self, val):
		self.val = val
		self.has_changed = True
		t = '{}{}'.format(self.prefix, val)
		self.canvas.itemconfig(self.text_obj, text=t)



	def check_text(self, text):
		try:
			return int(text) <= self.max_val
		except:
			return False



























