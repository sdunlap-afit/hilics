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
	from Tkinter.font import Font
except ImportError:
	import tkinter as tk
	from tkinter.font import Font


from PIL import Image, ImageTk


import threading
import time

from sims.DoorSim import DoorSim
from widgets.AlarmCircle import AlarmCircle


class Door(tk.Frame):
	
	
	
	def __init__(self, master=None, default_bg=None, default_fg=None, width=800, height=480):
		self.master = master
		super().__init__(master)

		self.default_bg = default_bg
		self.default_fg = default_fg
		
		self.high_color = '#EC7600'
		self.low_color = '#678CB1'
		self.alarm_color = '#C00000'
		self.door_color = '#152020'
		self.green_color = '#93C763'
		
		self.default_width = width
		self.default_height = height
		self.door_pos = 0
		self.panels = []
		self.doorsim = DoorSim()
		
		self.pack()
		self.create_widgets()
	
		self.running = True
		self.thread = threading.Thread(target=self.worker_thread)
		self.thread.setDaemon(True)
		self.thread.start()
	
	
		self.thread2 = threading.Thread(target=self.sim_thread)
		self.thread2.setDaemon(True)
		self.thread2.start()
	
	
	
	def clean_up(self):
		self.running = False
		self.thread.join(1.0)
		self.thread2.join(1.0)
		self.doorsim.close()
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
		
		
	
	
	
	def sim_thread(self):
		while self.running:
		
			try:
				
				self.doorsim.update()
				
				time.sleep(0.01)


			except Exception as e: 
				print(e)
	
	
	
	
	
	def worker_thread(self):

		while self.running:
		
			try:
				
				self.update_buttons()
				self.update_indicators()
				self.update_motor()
				self.update_alarms()
				
				self.update_door(int(self.doorsim.doorpos))
				
				self.update_switches()
				
				time.sleep(0.01)

			except Exception as e: 
				print(e)

	
	def update_alarms(self):
		
		self.top_crash_alarm.update(self.doorsim.top_alarm)
		self.btm_crash_alarm.update(self.doorsim.btm_alarm)
		self.motor_alarm.update(self.doorsim.motor_alarm)
		
		

	def update_switches(self):
	
		if self.doorsim.open_switch:
			self.canvas.itemconfig(self.open_switch, fill=self.high_color, outline=self.high_color)
		else:
			self.canvas.itemconfig(self.open_switch, fill=self.low_color , outline=self.low_color )
			
		if self.doorsim.closed_switch:
			self.canvas.itemconfig(self.close_switch, fill=self.high_color, outline=self.high_color)
		else:
			self.canvas.itemconfig(self.close_switch, fill=self.low_color , outline=self.low_color)

		
		if self.doorsim.prox_switch:
			self.canvas.itemconfig(self.prox_switch, fill=self.high_color, outline=self.high_color)
			self.canvas.itemconfig(self.car, state='normal')
		else:
			self.canvas.itemconfig(self.prox_switch, fill=self.low_color , outline=self.low_color)
			self.canvas.itemconfig(self.car, state='hidden')
		
		
		if self.doorsim.impact_switch:
			self.canvas.itemconfig(self.impact_switch, fill=self.high_color, outline=self.high_color)
			self.canvas.itemconfig(self.explosion, state='normal')
		else:
			self.canvas.itemconfig(self.impact_switch, fill=self.low_color , outline=self.low_color)
			self.canvas.itemconfig(self.explosion, state='hidden')
		
		
			
			
			
	def update_motor(self):
	
		if self.doorsim.motor_up:
			self.canvas.itemconfig(self.motor_up, fill=self.high_color, outline=self.high_color)
		else:                                                         
			self.canvas.itemconfig(self.motor_up, fill=self.low_color , outline=self.low_color )
			
		if self.doorsim.motor_down:
			self.canvas.itemconfig(self.motor_down, fill=self.high_color, outline=self.high_color)
		else:                                                           
			self.canvas.itemconfig(self.motor_down, fill=self.low_color , outline=self.low_color )

			
			


	def update_buttons(self):
	 
		if self.doorsim.open_btn:
			self.canvas.itemconfig(self.open_btn, fill=self.high_color, outline=self.high_color)
		else:                                                         
			self.canvas.itemconfig(self.open_btn, fill=self.low_color , outline=self.low_color )
		
		if self.doorsim.close_btn:
			self.canvas.itemconfig(self.close_btn, fill=self.high_color, outline=self.high_color)
		else:                                                          
			self.canvas.itemconfig(self.close_btn, fill=self.low_color , outline=self.low_color )
		
		if self.doorsim.stop_btn:
			self.canvas.itemconfig(self.stop_btn, fill=self.high_color, outline=self.high_color)
		else:                                                         
			self.canvas.itemconfig(self.stop_btn, fill=self.low_color , outline=self.low_color )
	
	
	def update_indicators(self):
	 
		if self.doorsim.open_ind:
			self.canvas.itemconfig(self.open_ind, fill=self.high_color, outline=self.high_color)
		else:                                                         
			self.canvas.itemconfig(self.open_ind, fill=self.low_color , outline=self.low_color )
		
		if self.doorsim.closed_ind:
			self.canvas.itemconfig(self.closed_ind, fill=self.high_color, outline=self.high_color)
		else:                                                           
			self.canvas.itemconfig(self.closed_ind, fill=self.low_color , outline=self.low_color )
		
		if self.doorsim.ajar_ind:
			self.canvas.itemconfig(self.ajar_ind, fill=self.high_color, outline=self.high_color)
		else:                                                         
			self.canvas.itemconfig(self.ajar_ind, fill=self.low_color , outline=self.low_color )
	
	

	def update_door(self, pos):
		
		# Dead zone at top of door (stops from opening completely)
		#if pos < 10:
		#	pos = 10
		
		if not self.door_pos == pos:
		
			self.door_pos = pos  # 0 - 100
			panel_height = 75   # pixels

			pos = int(pos * 0.9) + 10.0
			
			coords = self.canvas.coords(self.door_rect)
			startx = coords[0] + 2
			starty = coords[1] + 2
			endx   = coords[2] - 2
			endy   = coords[3] - 2
			
			
			if len(self.panels) < 1:
				
				self.canvas.tag_raise(self.car)
				
				num_panels = 1 + int((endy - starty) / panel_height)
				
				for __ in range(0, num_panels):
					p = self.canvas.create_rectangle(0, 0, 1, 1, outline=self.door_color, fill=self.door_color, state='hidden')
					self.panels.append(p)
					
				self.canvas.tag_raise(self.explosion)

				#print(self.panels)
					
			next_panel_endy = starty + int(((endy - starty) * pos) / 100)
			
			for p in self.panels:
				
				if next_panel_endy < starty:
					self.canvas.itemconfig(p, state='hidden')
					
				else:
					
					sy = next_panel_endy - panel_height
					ey = next_panel_endy
					
					next_panel_endy = sy - 2
					
					if sy < starty:
						sy = starty
				
					self.canvas.coords(p, startx, sy, endx, ey)
					self.canvas.itemconfig(p, state='normal')
				
				
					
			#self.canvas.pack()

	
	
	
	
	def open_btn_click(self, event):
		self.doorsim.open_btn = not self.doorsim.open_btn
		
	def close_btn_click(self, event):
		self.doorsim.close_btn = not self.doorsim.close_btn
	
	def stop_btn_click(self, event):
		self.doorsim.stop_btn = not self.doorsim.stop_btn
		
		
		
	def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):

		points = [x1+radius, y1,
					x1+radius, y1,
					x2-radius, y1,
					x2-radius, y1,
					x2, y1,
					x2, y1+radius,
					x2, y1+radius,
					x2, y2-radius,
					x2, y2-radius,
					x2, y2,
					x2-radius, y2,
					x2-radius, y2,
					x1+radius, y2,
					x1+radius, y2,
					x1, y2,
					x1, y2-radius,
					x1, y2-radius,
					x1, y1+radius,
					x1, y1+radius,
					x1, y1]

		return canvas.create_polygon(points, kwargs, smooth=True)
	
	
	
	def setup_frame1(self):
		
		frame = tk.Frame(self, width=800, height=400)
		self.config_frame(frame)
		frame.grid(row = 0, column=0, columnspan=1, rowspan=1)
		
		
		# lab = tk.Label(frame, text='Door', font=("Helvetica", 16))
		# self.config_label(lab)
		# lab.grid(column=1, row=0, columnspan=1, pady=10)
		
		# frame.grid_columnconfigure(0, weight=1)
		# frame.grid_columnconfigure(2, weight=1)
		
		
		self.canvas = tk.Canvas(frame, width=800, height=400, bd=0, highlightthickness=0, relief='ridge')
		self.config_bg(self.canvas)
		
		
		
		##########  Door Frame  ##########
		
		width = 300
		height = 300
		sx = (800 - width) / 2
		sy = (400 - height) / 2
		ex = sx + width
		ey = sy + height
		coords = [sx, sy, ex, ey]
		
		self.door_rect = self.canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], outline=self.default_fg, fill=self.default_fg)
		
		
		font = 'Helvetica 16 bold'
		r = 15
		self.btm_crash_alarm = AlarmCircle(self.canvas, sx + 100, ey + 25, r, self.alarm_color, self.default_bg, 'CRASH!', font)
		self.top_crash_alarm = AlarmCircle(self.canvas, sx + 100, sy - 25, r, self.alarm_color, self.default_bg, 'CRASH!', font)
		

		x = sx + (ex - sx) / 2
		y = ey - 10
			
		img = Image.open('images/explosion.png')
		img.thumbnail((250, 250), Image.ANTIALIAS)
		self.explosion_img_junk = ImageTk.PhotoImage(img)
		
		self.explosion = self.canvas.create_image(x, y, anchor='s', image=self.explosion_img_junk)
		

		img = Image.open('images/Car1.png')
		img.thumbnail((250, 250), Image.ANTIALIAS)
		self.car_img_junk = ImageTk.PhotoImage(img)
		
		self.car = self.canvas.create_image(x, y, anchor='s', image=self.car_img_junk)
		
		
		
		
		##########  Limit Switches  ##########
		
		sx = coords[0] - 30
		sy = coords[1] + 20
		ex = sx + 20
		ey = sy + 20
		
		self.open_switch = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(sx+10, sy-8, anchor='c', text = 'I:0/0', fill=self.default_fg)
		self.canvas.create_text(sx-5, sy+10, anchor='e', text = 'Limit', font=("Helvetica", 10), fill=self.default_fg)
		
		sx = coords[0] - 30
		sy = coords[3] - 40
		ex = sx + 20
		ey = sy + 20
		
		self.close_switch = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(sx+10, sy-8, anchor='c', text = 'I:0/1', fill=self.default_fg)
		self.canvas.create_text(sx-5, sy+10, anchor='e', text = 'Limit', font=("Helvetica", 10), fill=self.default_fg)
		
		
		
		sx = coords[2] + 10
		sy = coords[3] - (height / 2) - 10
		ex = sx + 20
		ey = sy + 20
		
		self.impact_switch = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.low_color, fill=self.low_color)
		
		self.canvas.create_text(sx+10, sy-8, anchor='c', text = 'I:0/6', fill=self.default_fg)
		self.canvas.create_text(ex+5, sy+10, anchor='w', text = 'Impact', font=("Helvetica", 10), fill=self.default_fg)
		
		
		
		
		
		sx = coords[2] + 10
		sy = coords[3] - 40
		ex = sx + 20
		ey = sy + 20
		
		self.prox_switch = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.low_color, fill=self.low_color)
		
		self.canvas.create_text(sx+10, sy-8, anchor='c', text = 'I:0/5', fill=self.default_fg)
		self.canvas.create_text(ex+5, sy+10, anchor='w', text = 'Proximity', font=("Helvetica", 10), fill=self.default_fg)
		
		
		
		
		
		
		
		##########  Motor Indicators  ##########
		
		sx = coords[2] + 75
		sy = coords[1] + 10
		ex = sx + 50
		ey = sy + 40
		
		self.motor_up = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.default_fg, fill=self.low_color)
		
		
		
		
		self.motor_alarm = AlarmCircle(self.canvas, sx, ey + 25, r, self.alarm_color, self.default_bg, 'ALARM!', font)
		
		
		
		
		
		m = sx + (ex - sx) / 2
		offset = 9
		self.canvas.create_line(sx+offset, ey-offset, m, sy+offset, fill=self.default_bg, width=5)
		self.canvas.create_line(m, sy+offset, ex-offset, ey-offset, fill=self.default_bg, width=5)
		self.canvas.create_text(sx-5, sy+20, anchor='e', text = 'O:0/0', fill=self.default_fg)
		
		sx = sx + 52
		ex = sx + 50
		ey = sy + 40
				
		self.motor_down = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.default_fg, fill=self.low_color)
		
		m = sx + (ex - sx) / 2
		self.canvas.create_line(sx+offset, sy+offset, m, ey-offset, fill=self.default_bg, width=5)
		self.canvas.create_line(m, ey-offset, ex-offset, sy+offset, fill=self.default_bg, width=5)
		
		self.canvas.create_text(ex+5, sy+20, anchor='w', text = 'O:0/1', fill=self.default_fg)
		
		
		self.canvas.create_text(sx-1, sy-15, anchor='c', text = 'Motor', font=("Helvetica", 14), fill=self.default_fg)
		
		
		
		
		
		
		##########  Button Panel  ##########
		
		ht = 200
		wd = 125
		sx = 10
		sy = 380 - ht
		ex = sx + wd
		ey = sy + ht
		
		#rect = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.default_fg, fill=self.default_fg)
		self.round_rectangle(self.canvas, sx, sy, ex, ey, radius=50, outline=self.default_fg, fill=self.default_fg)
		
		
		
		x = sx + ((ex - sx) / 2)
		y = sy + 20
		self.canvas.create_text(x, y, anchor='c', text = 'Buttons', font=("Helvetica", 14), fill=self.default_bg)
		
		
		
		r = 20
		x = sx + ((ex - sx) / 2)
		y = sy + 15 + (1 * (ey - sy) / 4)
		
		self.open_btn = self.round_rectangle(self.canvas, x-r, y-r, x+r, y+r, radius=20, outline=self.default_fg, fill=self.low_color)
		#self.open_btn = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.default_fg, fill=self.low_color)
		
		
		self.canvas.tag_bind(self.open_btn, '<Button-1>', self.open_btn_click)
		self.canvas.create_text(x - r - 2, y, anchor='e', text = 'I:0/2', fill=self.default_bg)
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'OPEN', fill=self.default_bg)
		
		x = sx + ((ex - sx) / 2)
		y = sy + 15 + (2 * (ey - sy) / 4)
		self.close_btn = self.round_rectangle(self.canvas, x-r, y-r, x+r, y+r, radius=20, outline=self.default_fg, fill=self.low_color)
		self.canvas.tag_bind(self.close_btn, '<Button-1>', self.close_btn_click)
		self.canvas.create_text(x - r - 2, y, anchor='e', text = 'I:0/3', fill=self.default_bg)
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'CLOSE', fill=self.default_bg)
		
		x = sx + ((ex - sx) / 2)
		y = sy + 15 + (3 * (ey - sy) / 4)
		self.stop_btn = self.round_rectangle(self.canvas, x-r, y-r, x+r, y+r, radius=20, outline=self.default_fg, fill=self.low_color)
		self.canvas.tag_bind(self.stop_btn, '<Button-1>', self.stop_btn_click)
		self.canvas.create_text(x - r - 2, y, anchor='e', text = 'I:0/4', fill=self.default_bg)
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'STOP', fill=self.default_bg)
		
		
		
		
		##########  Car Button  ##########
		
		w = 65
		h = 40
		x = (sx + ((ex - sx) / 2)) - w/2
		y = sy - h - h
		rect = self.round_rectangle(self.canvas, x, y, x+w, y+h, radius=20, outline=self.green_color, fill=self.green_color)
		lab = self.canvas.create_text(x + w/2, y+h/2, anchor='c', text = 'Car', fill=self.default_bg, font='Helvetica 12 bold')
		
		self.canvas.tag_bind(rect, '<Button-1>', self.doorsim.begin_car)
		self.canvas.tag_bind(lab, '<Button-1>', self.doorsim.begin_car)
		
		
		
		
		
		
		
		
		
		##########  Indicator Panel  ##########
		
		ht = 200
		wd = 125
		sx = 790 - wd
		sy = 380 - ht
		ex = sx + wd
		ey = sy + ht
		
		#rect = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.default_fg, fill=self.default_fg)
		self.round_rectangle(self.canvas, sx, sy, ex, ey, radius=50, outline=self.default_fg, fill=self.default_fg)
		
		
		
		x = sx + ((ex - sx) / 2)
		y = sy + 20
		self.canvas.create_text(x, y, anchor='c', text = 'Indicators', font=("Helvetica", 14), fill=self.default_bg)
		
		
		
		r = 20
		
		x = sx + ((ex - sx) / 2)
		y = sy + 15 + (1 * (ey - sy) / 4)
		self.open_ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(x - r - 2, y, anchor='e', text = 'O:0/2', fill=self.default_bg)
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'OPEN', fill=self.default_bg)
		
		x = sx + ((ex - sx) / 2)
		y = sy + 15 + (2 * (ey - sy) / 4)
		self.closed_ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(x - r - 2, y, anchor='e', text = 'O:0/3', fill=self.default_bg)
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'CLOSE', fill=self.default_bg)
		
		x = sx + ((ex - sx) / 2)
		y = sy + 15 + (3 * (ey - sy) / 4)
		self.ajar_ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(x - r - 2, y, anchor='e', text = 'O:0/4', fill=self.default_bg)
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'AJAR', fill=self.default_bg)
		
		
		
		
		
		self.canvas.pack()
		
	
	
	def normal_speed_clk(self):
		self.doorsim.time_scale = 1.0
	
	def double_speed_clk(self):
		self.doorsim.time_scale = 2.0
		
	def quad_speed_clk(self):
		self.doorsim.time_scale = 4.0
		
		
		
	def setup_bottom_frame(self):
		
		frame = tk.Frame(self, width=self.default_width, height=80)
		self.config_frame(frame)
		frame.grid(row = 1, column=0, columnspan=1, rowspan=1)
		
		
		self.normal_speed = tk.Button(frame, text='x1 Speed', command=self.normal_speed_clk)
		self.config_btn(self.normal_speed)
		self.normal_speed.place(relx=0.10, rely=0.5, anchor=tk.CENTER)

		self.quad_speed = tk.Button(frame, text='x4 Speed', command=self.quad_speed_clk)
		self.config_btn(self.quad_speed)
		self.quad_speed.place(relx=0.280, rely=0.5, anchor=tk.CENTER)
		

		self.ccrCanvas = tk.Canvas(frame, bg=self.default_bg, width=77,height=77, bd=0, highlightthickness=0, relief='ridge')
		self.ccrCanvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		img = Image.open('./images/ccr_logo.png').resize((77, 77), Image.ANTIALIAS)
		self.ccrImage = ImageTk.PhotoImage(img)
		self.ccrCanvas.create_image(0,0,image=self.ccrImage,anchor="nw")

		self.logoCanvas = tk.Canvas(frame, bg=self.default_bg, width=180,height=77, bd=0, highlightthickness=0, relief='ridge')
		self.logoCanvas.place(relx=0.680, rely=0.5, anchor=tk.CENTER)
		self.logoImage = ImageTk.PhotoImage(file='./images/afit_logo.png')
		self.logoCanvas.create_image(0,0,image=self.logoImage,anchor="nw")
		
		self.quit = tk.Button(frame, text='Back', command=self.clean_up)
		self.config_btn(self.quit)
		self.quit.place(relx=0.9, rely=0.5, anchor=tk.CENTER)
		
		
	
	def create_widgets(self):
	 
	
		self.master.minsize(width=self.default_width, height=self.default_height)
		self.master.maxsize(width=self.default_width, height=self.default_height)

		self.setup_frame1()
		self.setup_bottom_frame()

		

		
		

		

		
		

		
		


