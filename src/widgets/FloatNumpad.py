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



class FloatNumpad():
	
	
	def __init__(self, canvas, default_text, font, x, y, width, height, bg, fg, default_val=0, max_val=100.0):
		self.canvas = canvas
		
		self.frame_sx = x
		self.frame_sy = y
		self.frame_ex = x + width
		self.frame_ey = y + height
		self.frame_radius = (height + width) / 16
		
		self.width = width
		self.height = height
		
		self.default_text = default_text
		self.font = font
		
		self.bg = bg
		self.fg = fg
		
		self.padding = 4
		self.row_height = (height - (6 * self.padding)) / 5
		self.col_width = (width - (4 * self.padding)) / 3
		
		self.val = default_val
		self.current_text = self.default_text
		self.has_changed = True
		
		self.max_val = max_val
		
		self.create_frame()
		self.create_textrow()
		self.create_buttons()
		
		

	def create_frame(self):
		x1 = self.frame_sx
		y1 = self.frame_sy
		x2 = self.frame_ex
		y2 = self.frame_ey
		r = self.frame_radius
		
		self.frame_rect = Rounded_Rect(self.canvas, x1, y1, x2, y2, r, outline=self.fg, fill=self.fg)
		
		

	def create_textrow(self):
		x1 = self.frame_sx + self.padding
		y1 = self.frame_sy + self.padding
		
		x2 = x1 + self.col_width + self.padding + self.col_width
		y2 = y1 + self.row_height
		r = self.frame_radius / 2
		
		self.textrect = Rounded_Rect(self.canvas, x1, y1, x2, y2, r, outline=self.bg, fill=self.bg)
		
		cx = x1 + (x2 - x1) / 2
		cy = y1 + (y2 - y1) / 2
		self.text_obj = self.canvas.create_text(cx, cy, anchor='c', text=self.current_text, fill=self.fg, font=self.font)
		
		x1 = x2 + self.padding
		# y1 = y1
		x2 = x1 + self.col_width
		# y2 = y2
		
		
		btn = Rounded_Rect(self.canvas, x1, y1, x2, y2, r, outline=self.bg, fill=self.bg)
		
		cx = x1 + (x2 - x1) / 2
		cy = y1 + (y2 - y1) / 2

		t = 'Bck'
		txt = self.canvas.create_text(cx, cy, anchor='c', text=t, fill=self.fg, font=self.font)
		
		self.canvas.tag_bind(txt, '<Button-1>', lambda e, t=t: self.click(text=t))
		self.canvas.tag_bind(btn.id, '<Button-1>', lambda e, t=t: self.click(text=t))
		
		
		
	def create_buttons(self):
		labels = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['0', '.', 'Ent']]
		
		rad = self.frame_radius / 2
		sy = self.frame_sy + self.padding + self.row_height + self.padding
		sx = self.frame_sx + self.padding
		
		for c in range(0, 3):
		
			for r in range(0, 4):
				
				x1 = sx + (c * self.col_width) + (c * self.padding)
				x2 = x1 + self.col_width
				
				y1 = sy + (r * self.row_height) + (r * self.padding)
				y2 = y1 + self.row_height
						
				btn = Rounded_Rect(self.canvas, x1, y1, x2, y2, rad, outline=self.bg, fill=self.bg)

				cx = x1 + (x2 - x1) / 2
				cy = y1 + (y2 - y1) / 2
		
				t = labels[r][c]
				txt = self.canvas.create_text(cx, cy, anchor='c', text=t, fill=self.fg, font=self.font)
				
				self.canvas.tag_bind(txt, '<Button-1>', lambda e, t=t: self.click(text=t))
				self.canvas.tag_bind(btn.id, '<Button-1>', lambda e, t=t: self.click(text=t))





	def click(self, text):
		
		if self.current_text == self.default_text:
			self.current_text = ''
	
		if text == 'Bck':
			
			self.current_text = self.current_text[:-1]
			
			if len(self.current_text) < 1:
				self.current_text = self.default_text
				
		elif text == 'Ent':
			try:
				self.val = float(self.current_text)
				self.has_changed = True				
			except:
				pass
				
			self.current_text = self.default_text
			
		else:
			t = self.current_text + text
			if self.check_text(t):
				self.current_text = t
		
		self.canvas.itemconfig(self.text_obj, text=self.current_text)



		
	def check_text(self, text):
		try:
			return float(text) <= self.max_val and len(text) < 6
		except:
			return False




























