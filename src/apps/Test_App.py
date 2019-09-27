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

from sims.SimIO import SimIO	
from widgets.Dial_Canvas import Dial_Canvas
from widgets.FloatNumpad import FloatNumpad
from widgets.Tank import Tank
from widgets.Graph import Graph


import threading
import time
import math



class TestApp(tk.Frame):
	
	
	
	def __init__(self, master=None, default_bg=None, default_fg=None):
		self.master = master
		
		self.screen_w = master.winfo_screenwidth()
		self.screen_h = master.winfo_screenheight()
		
		self.default_bg = default_bg
		self.default_fg = default_fg
		
		self.high_color = '#EC7600'
		self.low_color = '#678CB1'
		
		self.water_color = '#07A8E4'
		
		self.simio = SimIO(verbose=False)

		self.val = 0.0
		
		super().__init__(master)
		self.pack()
		self.create_widgets()
	
		self.running = True
		self.thread = threading.Thread(target=self.worker_thread)
		self.thread.setDaemon(True)
		self.thread.start()
		
	
	
	# Convert 0-100 to screen size and position
	def to_screen(self, sx, sy, ex, ey):
		
		sx = self.to_width(sx)
		ex = self.to_width(ex)
		
		sy = self.to_height(sy)
		ey = self.to_height(ey)
		
		return sx, sy, ex, ey
	
	
	def to_width(self, w):
		return int((w * self.screen_w) / 100.0 )
		
		
	def to_height(self, h):
		return int((h * self.screen_h) / 100.0 )
		
		
	
	def clean_up(self):
		self.running = False
		self.thread.join(1.0)
		self.simio.close()
		self.master.destroy()
	
	

	def config_bg(self, wid):
		if not self.default_bg is None:
			wid['bg'] = self.default_bg
		


	def config_fg(self, wid):
		if not self.default_fg is None:
			wid['fg'] = self.default_fg
	
	
	
	def config_frame(self, frame):
		frame['borderwidth'] = 1
		frame['relief'] = tk.RIDGE
		frame.pack_propagate(0)
		frame.grid_propagate(0)
		
		self.config_bg(frame)
	
		
	
	def config_btn(self, btn):
		btn['font'] = Font(root=self.master, family='Helvetica', size=18)
		btn['width'] = 8
		btn['height'] = 2
		btn['activebackground'] = self.default_bg
		btn['activeforeground'] = self.default_fg
		btn['bd'] = 0
		btn['highlightthickness'] = 1
		btn['relief'] = 'ridge'
		self.config_bg(btn)
		self.config_fg(btn)
	

	
	def config_label(self, lab):
		self.config_bg(lab)
		self.config_fg(lab)
	
	
	
	def worker_thread(self):
	
		while self.running:
		
			try:
				time.sleep(0.1)
				
				self.val += 1
				
				if self.val > 100:
					self.val = 0
				
				self.graph.add_point(0, self.val)
			
			except Exception as e: 
				print(e)
		
		#print('DONE')
	
	
	
	def setup_frame1(self):
		
		w = self.to_width(100)
		h = self.to_height(85)
		frame = tk.Frame(self, width=w, height=h)
		self.config_frame(frame)
		frame.grid(row = 0, column=0, columnspan=2, rowspan=1)		
		
		self.canvas = tk.Canvas(frame, width=w, height=h, bd=0, highlightthickness=0, relief='ridge')
		self.config_bg(self.canvas)
		
		
		width = self.to_width(50)
		height = self.to_height(50)
		x = (self.to_width(100) - width) / 2
		y = (self.to_height(85) - height) / 2

		self.graph = Graph(self.canvas, x, y, width, height, self.default_fg, self.default_bg, 100, 30)
		self.graph.add_graph('#0000C0')
		
		self.canvas.pack()
	


	def setup_frame5(self):
		
		w = self.to_width(50)
		h = self.to_height(15)
		
		frame = tk.Frame(self, width=w, height=h)
		self.config_frame(frame)
		frame.grid(row = 1, column=0, columnspan=1, rowspan=1)
		
		

	def setup_bottom_frame(self):
		w = self.to_width(50)
		h = self.to_height(15)
		
		frame = tk.Frame(self, width=w, height=h)
		self.config_frame(frame)
		frame.grid(row = 1, column=1, columnspan=1, rowspan=1)
		
		
		self.quit = tk.Button(frame, text='Back', command=self.clean_up)
		self.config_btn(self.quit)
		self.quit.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
	
	
	
	def create_widgets(self):
	
		self.master.minsize(width=800, height=480)
		self.master.maxsize(width=800, height=480)

		self.setup_frame1()
		
		self.setup_frame5()
		self.setup_bottom_frame()

		

