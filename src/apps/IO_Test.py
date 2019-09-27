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

import threading
import time

from PIL import ImageTk, Image

from sims.SimIO import SimIO
from widgets.Dial_Canvas import Dial_Canvas


class IO_Test(tk.Frame):
	
	
	
	def __init__(self, master=None, default_bg=None, default_fg=None):
		self.master = master
		super().__init__(master)

		self.default_bg = default_bg
		self.default_fg = default_fg
		
		self.high_color = '#EC7600'
		self.low_color = '#678CB1'
		
		self.simio = SimIO(verbose=False)

		
		self.dig_inputs = []
		self.dig_input_btns = []
		
		self.relay_outs = []
		self.dig_output_btns = []
		
		self.dials = []
		
		self.pack()
		self.create_widgets()
	
		self.running = True
		self.thread = threading.Thread(target=self.worker_thread)
		self.thread.setDaemon(True)
		self.thread.start()
	
	
	
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
				relay_vals = self.simio.read_relay_outs()
				ang_out_vals = self.simio.read_ang_outs()
				
				for i in range(0, min(len(self.dials), len(ang_out_vals))):
					self.dials[i].update(ang_out_vals[i])
				
				if not relay_vals == self.relay_outs:
					self.relay_outs = relay_vals
					
					for i in range(0, len(self.dig_output_btns)):
					
						if self.relay_outs[i]:
							#self.dig_output_btns[i].config(relief='sunken')
							# Orange
							self.dig_output_btns[i].config(bg=self.high_color)
							self.dig_output_btns[i].config(activebackground=self.high_color)
							self.dig_output_btns[i].config(state = 'normal')
							 
						else:
							#self.dig_output_btns[i].config(relief='raised')
							# Light Blue
							self.dig_output_btns[i].config(bg=self.low_color)
							self.dig_output_btns[i].config(activebackground=self.low_color)
							self.dig_output_btns[i].config(state = 'normal')
					
		
				v1 = float(self.scale1_var.get())
				v2 = float(self.scale2_var.get())
				
				vals = [int(v1 * 409.5), int(v2 * 409.5)]
		
				self.simio.write_ang_ins(vals)
				self.simio.write_dig_ins(self.dig_inputs)
				
				time.sleep(0.01)
				
			except Exception as e: 
				print(e)
		
		#print('DONE')
		
	
	
	
	def toggle(self, index):
		
		self.dig_inputs[index] = not self.dig_inputs[index]
		
		self.simio.write_dig_ins(self.dig_inputs)
		
		if self.dig_inputs[index]:
			#self.dig_input_btns[index].config(relief='sunken')
			# Orange
			self.dig_input_btns[index].config(bg=self.high_color)
			self.dig_input_btns[index].config(activebackground=self.high_color)
						
			self.dig_input_btns[index].config(state = 'normal')
			 
		else:
			#self.dig_input_btns[index].config(relief='raised')
			# Light Blue
			self.dig_input_btns[index].config(bg=self.low_color)
			self.dig_input_btns[index].config(activebackground=self.low_color)
			self.dig_input_btns[index].config(state = 'normal')
		
		
	
	def ignore(self, index):
		self.dig_output_btns[index].config(state = 'normal')
	
	
	
	
	def setup_frame1(self):
		
		frame = tk.Frame(self, width=400, height=225)
		self.config_frame(frame)
		frame.grid(row = 0, column=0, columnspan=1, rowspan=1)		
		
		lab = tk.Label(frame, text='Digital Inputs', font=('Helvetica', 16))
		self.config_label(lab)
		lab.grid(column=1, row=0, columnspan=5, pady=2)
		
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_columnconfigure(6, weight=1)
		
		for i in range(0, 10):
			
			lab = tk.Label(frame, text='I:0/{} - '.format(i))
			self.config_label(lab)
			
			
			
			img1 = tk.PhotoImage(width=1, height=1)
			b = tk.Button(frame, image=img1, borderwidth=0, relief=tk.FLAT, bg=self.low_color, fg=self.low_color, width=50, height=27, command=lambda i=i: self.toggle(i))
			b['activebackground'] = self.low_color
			b['bd'] = 0
			b['highlightthickness'] = 0
			b['relief'] = 'ridge'
			
			b.image = img1
			
			if i < 5:
				lab.grid(column=1, row=(i + 1), padx=1, sticky=tk.E)
				b.grid(column=2, row=(i+1), padx=20, pady=2, sticky=tk.W)
				
				self.dig_inputs.append(False)
				self.dig_input_btns.append(b)
				
				lab = tk.Label(frame, text='       ')
				self.config_label(lab)
				lab.grid(column=3, row=(i + 1), padx=1)
				
			else:
				lab.grid(column=4, row=(i + 1 - 5), padx=1, sticky=tk.E)
				b.grid(column=5, row=(i + 1 - 5), padx=20, pady=2, sticky=tk.W)
				
				self.dig_inputs.append(False)
				self.dig_input_btns.append(b)





	def setup_frame2(self):
		
		frame = tk.Frame(self, width=400, height=175)
		self.config_frame(frame)
		frame.grid(row = 1, column=0, columnspan=1, rowspan=1)
					
		lab = tk.Label(frame, text='Relay Outputs', font=('Helvetica', 16))
		self.config_label(lab)
		lab.grid(column=1, row=0, columnspan=2, pady=2)
		
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_columnconfigure(3, weight=1)
		
		for i in range(0, 6):
			
			lab = tk.Label(frame, text='O:0/{} - '.format(i))
			self.config_label(lab)
			lab.grid(column=1, row=(i + 1), padx=10)
			
			
			img1 = tk.PhotoImage(width=1, height=1)
			b = tk.Button(frame, image=img1, borderwidth=0, relief=tk.FLAT, bg=self.low_color, fg=self.low_color, width=30, height=17, command=lambda i=i: self.ignore(i))
			b['activebackground'] = self.low_color
			b['bd'] = 0
			b['highlightthickness'] = 0
			b['relief'] = 'ridge'
			b.image = img1
			
			b.grid(column=2, row=(i+1), pady=2)
			
			self.relay_outs.append(False)
			self.dig_output_btns.append(b)

	
	
	
	
	
	
	
	
	
	
		
		
		
	def setup_frame3(self):
		
		frame = tk.Frame(self, width=400, height=225)
		self.config_frame(frame)
		frame.grid(row = 0, column=1, columnspan=2, rowspan=1)
					
		lab = tk.Label(frame, text='Analog Outputs', font=('Helvetica', 16))
		self.config_label(lab)
		lab.grid(column=1, row=0, columnspan=2, pady=2)
		
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_columnconfigure(3, weight=1)
		
		
		
		dial_canvas = Dial_Canvas(frame, diameter=90, text='O:1.0', bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=10.0, dead_angle=120.0)
		dial_canvas.grid(column=1, row=1, pady=2, padx=20)
		self.dials.append(dial_canvas)

		dial_canvas = Dial_Canvas(frame, diameter=90, text='O:1.1', bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=10.0, dead_angle=120.0)
		dial_canvas.grid(column=2, row=1, pady=2, padx=20)
		self.dials.append(dial_canvas)

		dial_canvas = Dial_Canvas(frame, diameter=90, text='O:1.2', bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=10.0, dead_angle=120.0)
		dial_canvas.grid(column=1, row=2, pady=2, padx=20)
		self.dials.append(dial_canvas)

		dial_canvas = Dial_Canvas(frame, diameter=90, text='O:1.3', bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=10.0, dead_angle=120.0)
		dial_canvas.grid(column=2, row=2, pady=2, padx=20)
		self.dials.append(dial_canvas)

		
		
		
		
		
		

	def iv1_left(self):
		if self.scale1_var.get() > 0.0:
			self.scale1_var.set(round(self.scale1_var.get() - 1.0, 1))
			
	def iv1_right(self):
		if self.scale1_var.get() < 10.0:
			self.scale1_var.set(round(self.scale1_var.get() + 1.0, 1))
			
	def iv2_left(self):
		if self.scale2_var.get() > 0.0:
			self.scale2_var.set(round(self.scale2_var.get() - 1.0, 1))
			
	def iv2_right(self):
		if self.scale2_var.get() < 10.0:
			self.scale2_var.set(round(self.scale2_var.get() + 1.0, 1))
	
		
		
		
	def setup_frame4(self):
		
		frame = tk.Frame(self, width=400, height=175)
		self.config_frame(frame)
		frame.grid(row = 1, column=1, columnspan=1, rowspan=1)
		
		
		lab = tk.Label(frame, text='Analog Inputs', font=('Helvetica', 16))
		self.config_label(lab)
		lab.grid(column=0, row=0, columnspan=5, pady=1)
		
		
		
		self.scale1_var = tk.DoubleVar()
		self.scale2_var = tk.DoubleVar()


		img1 = tk.PhotoImage(file='images/left_arrow.png')
		btn = tk.Button(frame, image=img1, command=self.iv1_left, height=50, width=20)
		btn['activebackground'] = self.default_bg
		btn.image = img1
		btn['bd'] = 0
		btn['highlightthickness'] = 0
		btn['relief'] = 'ridge'
		self.config_bg(btn)
		self.config_fg(btn)
		btn.grid(column=1, row=1, padx=2, sticky=tk.E+tk.S)
		
		
		img1 = tk.PhotoImage(file='images/right_arrow.png')
		btn = tk.Button(frame, image=img1, command=self.iv1_right, height=50, width=20)
		btn.image = img1
		btn['activebackground'] = self.default_bg
		btn['bd'] = 0
		btn['highlightthickness'] = 0
		btn['relief'] = 'ridge'
		self.config_bg(btn)
		self.config_fg(btn)
		btn.grid(column=3, row=1, padx=2, sticky=tk.W+tk.S)
		
		
		#self.scale = tk.Scale(frame, from_=0, to=10, resolution=0.1, command=self.onScale, sliderlength=20)
		scale = tk.Scale(frame, from_=0, to=10, resolution=0.1, variable=self.scale1_var, orient=tk.HORIZONTAL, sliderlength=30, length=225, width=40)
		scale['activebackground'] = self.default_bg
		scale['bd'] = 0
		scale['highlightthickness'] = 0
		scale['relief'] = 'ridge'
		self.config_bg(scale)
		self.config_fg(scale)
		scale.grid(column=2, row=1, padx=0, pady=3)

		lab = tk.Label(frame, text=0.0, textvariable=self.scale1_var)
		self.config_label(lab)		
		lab.grid(column=4, row=1, padx=5, pady=13, sticky=tk.S)
		
		lab = tk.Label(frame, text='I:0.4 - ')
		self.config_label(lab)
		lab.grid(column=0, row=1, padx=10, pady=18, sticky=tk.S)
		
		
		
		img1 = tk.PhotoImage(file='images/left_arrow.png')
		btn = tk.Button(frame, image=img1, command=self.iv2_left, height=50, width=20)
		btn.image = img1
		btn['activebackground'] = self.default_bg
		btn['bd'] = 0
		btn['highlightthickness'] = 0
		btn['relief'] = 'ridge'
		self.config_bg(btn)
		self.config_fg(btn)
		btn.grid(column=1, row=2, padx=2, sticky=tk.E+tk.S)
		
		img1 = tk.PhotoImage(file='images/right_arrow.png')
		btn = tk.Button(frame, image=img1, command=self.iv2_right, height=50, width=20)
		btn.image = img1
		btn['activebackground'] = self.default_bg
		btn['bd'] = 0
		btn['highlightthickness'] = 0
		btn['relief'] = 'ridge'
		self.config_bg(btn)
		self.config_fg(btn)
		btn.grid(column=3, row=2, padx=2, sticky=tk.W+tk.S)
		
		scale = tk.Scale(frame, from_=0, to=10, resolution=0.1, variable=self.scale2_var, orient=tk.HORIZONTAL, sliderlength=30, length=225, width=40)
		scale['activebackground'] = self.default_bg
		scale['bd'] = 0
		scale['highlightthickness'] = 0
		scale['relief'] = 'ridge'
		self.config_bg(scale)
		self.config_fg(scale)
		scale.grid(column=2, row=2, padx=0, pady=5)

		lab = tk.Label(frame, text=0.0, textvariable=self.scale2_var)
		self.config_label(lab)
		lab.grid(column=4, row=2, padx=5, pady=13, sticky=tk.S)
		
		lab = tk.Label(frame, text='I:0.5 - ')
		self.config_label(lab)
		lab.grid(column=0, row=2, padx=10, pady=18, sticky=tk.S)
		
		
		
	def setup_frame5(self):
		
		frame = tk.Frame(self, width=400, height=80)
		self.config_frame(frame)
		frame.grid(row = 2, column=0, columnspan=1, rowspan=1)
		
	
		
		
	def setup_bottom_left_frame(self):
		
		frame = tk.Frame(self, width=400, height=80)
		self.config_frame(frame)
		
		frame.grid(row = 2, column=0, columnspan=1, rowspan=1)
		
		self.ccrCanvas = tk.Canvas(frame, bg=self.default_bg, width=77,height=77, bd=0, highlightthickness=0, relief='ridge')
		self.ccrCanvas.place(relx=0.85, rely=0.5, anchor=tk.CENTER)
		img = Image.open('./images/ccr_logo.png').resize((77, 77), Image.ANTIALIAS)
		self.ccrImage = ImageTk.PhotoImage(img)
		self.ccrCanvas.create_image(0,0,image=self.ccrImage,anchor="nw")

		
	def setup_bottom_frame(self):
		
		frame = tk.Frame(self, width=400, height=80)
		self.config_frame(frame)
		frame.grid(row = 2, column=1, columnspan=1, rowspan=1)
		
		self.logoCanvas = tk.Canvas(frame, bg=self.default_bg, width=180,height=77, bd=0, highlightthickness=0, relief='ridge')
		self.logoCanvas.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
		self.logoImage = ImageTk.PhotoImage(file='./images/afit_logo.png')
		self.logoCanvas.create_image(0,0,image=self.logoImage,anchor="nw")

		self.quit = tk.Button(frame, text='Back', command=self.clean_up)
		self.config_btn(self.quit)
		self.quit.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
		
		
	
		
	def create_widgets(self):
	
		self.master.minsize(width=800, height=480)
		self.master.maxsize(width=800, height=480)

		self.setup_frame1()
		self.setup_frame2()
		self.setup_frame3()
		self.setup_frame4()
		self.setup_frame5()
		self.setup_bottom_left_frame()
		self.setup_bottom_frame()

		

		
		

		

		
		

		
	
