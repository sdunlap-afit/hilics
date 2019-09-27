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



class AlarmCircle():
	
	
	def __init__(self, canvas, x, y, radius, bg, fg, text, font):
		self.canvas = canvas
		
		self.x = x
		self.y = y
		self.radius = radius
		
		self.bg = bg
		self.fg = fg
		
		self.text = text
		self.font = font
		
		self.shown = False
		
		self.create_alarm()
		
	
	
	def create_alarm(self):
		x = self.x
		y = self.y
		r = self.radius
		
		self.ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.bg, fill=self.bg, state='hidden')
		
		self.ex_txt = self.canvas.create_text(x, y, anchor='c', text='!', fill=self.fg, font=self.font, state='hidden')
		
		x = x + self.radius + 5
		self.label = self.canvas.create_text(x, y, anchor='w', text=self.text, fill=self.bg, font=self.font, state='hidden')

	
	def update(self, shown):
		if shown:
			self.show()
		else:
			self.hide()

			
	def show(self):
		if not self.shown:
			self.shown = True
			self.canvas.itemconfig(self.ind, state='normal')
			self.canvas.itemconfig(self.ex_txt, state='normal')
			self.canvas.itemconfig(self.label, state='normal')

		
	def hide(self):
		if self.shown:
			self.shown = False
			self.canvas.itemconfig(self.ind, state='hidden')
			self.canvas.itemconfig(self.ex_txt, state='hidden')
			self.canvas.itemconfig(self.label, state='hidden')

























