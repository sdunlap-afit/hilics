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

import threading
import time

from PIL import ImageTk, Image

from sims.TankSim import TankSim
from widgets.Rounded_Rect import Rounded_Rect
from widgets.FloatNumpad import FloatNumpad
from widgets.Pipe import Pipe
from widgets.Tank import Tank
from widgets.AlarmCircle import AlarmCircle
from widgets.Graph import Graph
from widgets.Dial import Dial
from widgets.ButtonPanel import ButtonPanel



class Fluid_Tank(tk.Frame):
	
	
	
	def __init__(self, master=None, default_bg=None, default_fg=None, width=800, height=480):
		
		self.master = master
		super().__init__(master)
		
		self.default_bg = default_bg
		self.default_fg = default_fg
		
		self.high_color = '#EC7600'
		self.low_color = '#678CB1'
		
		self.alarm_color = '#C00000'
		
		self.water_color = '#07A8E4'

		self.level_sp = 20.0
		self.default_inflow_sp = 3
		
		self.default_width = width
		self.default_height = height
		self.pipe_diameter = 20
		self.tank_ht = 0
		
		self.tanksim = TankSim()
		self.water_rect = None
		
		self.last_update = 0
		
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
		self.tanksim.close()
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
				
				self.check_button_panels()
			
				self.tanksim.update()
				
				time.sleep(0.01)


			except Exception as e: 
				print(e)
	
	
	
	
	def worker_thread(self):

		while self.running:
		
			try:

				self.pump_dial.update(self.tanksim.pump.setpoint * 0.6)
				self.inflow_dial.update(self.tanksim.inflow_rate)
				self.valve_dial.update(self.tanksim.valve.position)
				
				self.update_setpoint()
				self.update_tank()
				self.update_pump()
				self.update_valve()
				self.update_floats()
				
				
				if self.tanksim.overflow:
					self.overflow_alarm.show()
				else:
					self.overflow_alarm.hide()
				
				self.graph.bring_to_top()
				
				time.sleep(0.01)


			except Exception as e: 
				print(e)

				
				
	def check_button_panels(self):
		if self.lev_butpan.has_changed:
			val = self.lev_butpan.val
			self.lev_butpan.has_changed = False
			
			self.tanksim.level_sp = val
			
		if self.inflow_butpan.has_changed:
			val = self.inflow_butpan.val * 10
			self.inflow_butpan.has_changed = False
			
			self.tanksim.inflow_sp = val
			

			
	def update_setpoint(self):
		
		sp = self.tanksim.level_sp
		self.tank_widget.update_setpoint(sp)
		
		
		

	def update_tank(self):
		
		ht = self.tanksim.water_level
		self.tank_widget.update(ht, not self.graph.is_full())
		
		t = time.time()
		
		if t - self.last_update > 1.0:
			self.last_update = t
			self.graph.add_point(0, ht)
			self.graph.add_point(1, self.tanksim.level_sp)
			self.graph.add_point(2, self.tanksim.inflow_rate * 10)
			self.graph.add_point(3, self.tanksim.inflow_sp)

			
		
			# self.graph.add_graph('#0000C0', 'Water Level', ("Helvetica", 8))
			# self.graph.add_graph('#00C000', 'Level SP', ("Helvetica", 8))
			# self.graph.add_graph('#C00000', 'Inflow Rate', ("Helvetica", 8))
			# self.graph.add_graph('#505050', 'Inflow SP', ("Helvetica", 8))
		
		
		
	
	def update_pump(self):
		
		enabled = self.tanksim.pump_on

		if enabled:
			self.canvas.itemconfig(self.in_pipe, fill=self.water_color, outline=self.water_color)
			self.canvas.itemconfig(self.in_pipe2, fill=self.water_color, outline=self.water_color)
			self.canvas.itemconfig(self.pump_rect.id, fill=self.high_color, outline=self.high_color)

		else:
			self.canvas.itemconfig(self.in_pipe, fill=self.default_fg, outline=self.default_fg)
			self.canvas.itemconfig(self.in_pipe2, fill=self.default_fg, outline=self.default_fg)
			self.canvas.itemconfig(self.pump_rect.id, fill=self.low_color, outline=self.low_color)
			
			
			
	def update_valve(self):
		
		enabled = self.tanksim.valve_open
		
		if enabled:
			self.canvas.itemconfig(self.out_pipe, fill=self.water_color, outline=self.water_color)
			self.canvas.itemconfig(self.valve_rect.id, fill=self.high_color, outline=self.high_color)

		else:
			self.canvas.itemconfig(self.out_pipe, fill=self.default_fg, outline=self.default_fg)
			self.canvas.itemconfig(self.valve_rect.id, fill=self.low_color, outline=self.low_color)


	def update_floats(self):
		self.tank_widget.update_float(self.low_ind, self.tanksim.low_float)
		self.tank_widget.update_float(self.high_ind, self.tanksim.high_float)
		self.tank_widget.update_float(self.high_high_ind, self.tanksim.high_high_float)
	

	
	
	
	
	def elbow_pipe(self, canvas, x1, y1, x2, y2, diameter=75, **kwargs):
		d = diameter
	
		points =   [x1, y1,
					x1, y1,
					x1, y2+d+d,
					x1, y2+d+d,
					x1, y2,
					x1+d+d, y2,
					x1+d+d, y2,
					x2, y2,
					x2, y2,
					x2, y2+d,
					x2, y2+d,
					x1+d+d, y2+d,
					x1+d+d, y2+d,
					x1+d, y2+d,
					x1+d, y2+d+d,
					x1+d, y2+d+d,
					x1+d, y1,
					x1+d, y1,
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
		
		
		
		##########  Tank  ##########
		
		
		width = 200
		height = 300
		x = (800 - width) / 3
		y = (400 - height) / 2

		font = 'Helvetica 8 bold'
		
		self.tank_widget = Tank(self.canvas, x, y, width, height, self.default_fg, self.water_color, self.default_bg, self.low_color, self.high_color)
		
		self.low_ind = self.tank_widget.add_float(self.tanksim.low_thresh, 12, 'L', font, 'I:0/0')
		self.high_ind = self.tank_widget.add_float(self.tanksim.high_thresh, 12, 'H', font, 'I:0/1')
		self.high_high_ind = self.tank_widget.add_float(self.tanksim.high_high_thresh, 12, 'HH', font, 'I:0/2')
		
		
		sx = self.tank_widget.sx
		sy = self.tank_widget.sy
		ex = self.tank_widget.ex
		ey = self.tank_widget.ey

		mx = (sx + ex) / 2
		self.canvas.create_text(mx, sy - 15, text='Level DPT: I:0.4', fill=self.default_fg, font='Helvetica 10 bold', anchor='c')
		
		
		
		##########  Graph  ##########
		
		w = 340
		h = 170
		self.graph = Graph(self.canvas, 800-w-25, 10, w, h, self.default_fg, self.default_bg, 100, 30, lines=True)
		self.graph.add_graph('#0000C0', 'Water Level', ("Helvetica", 8))
		self.graph.add_graph('#00C000', 'Level SP', ("Helvetica", 8))
		self.graph.add_graph('#C00000', 'Inflow Rate * 10', ("Helvetica", 8))
		self.graph.add_graph('#505050', 'Inflow SP * 10', ("Helvetica", 8))
		
		
		
		##########  Overflow Alarm  ##########
		
		font = 'Helvetica 16 bold'
		x = sx + 30
		y = sy - 20
		r = 15
		
		self.overflow_alarm = AlarmCircle(self.canvas, x, y, r, self.alarm_color, self.default_bg, 'OVERFLOW!', font)
		
		
		
		
		
		##########  Pipes  ##########
		
		
		### PUMP ###
		
		pipe_mid_y = self.tank_widget.sy + 20
		
		
		size = 40
		sx = 30
		ex = sx + size
		sy = pipe_mid_y - (size/2)
		ey = sy + size
		
		self.pump_rect = Rounded_Rect(self.canvas, sx, sy, ex, ey, radius=25, outline=self.low_color, fill=self.low_color)
		
		### PUMP ARROW ###
		mx = sx + ((ex - sx) / 2)
		my = sy + ((ey - sy) / 2)
		w = 15
		h = 12
		mex = mx + w
		self.canvas.create_line(mx - w, my,  mex, my, fill=self.default_bg, width=5)
		self.canvas.create_line(mex-2, my, mex-h, my-h , fill=self.default_bg, width=5)
		self.canvas.create_line(mex-2, my, mex-h, my+h , fill=self.default_bg, width=5)
		
		self.canvas.create_text(mx, sy - 15, text='Pump', fill=self.default_fg, font='Helvetica 10 bold', anchor='c')
		
		
		### Venturi Tube ###
		# Bronze - #cd7f32
		# Copper - #b87333
		
		
		w = 40
		h = self.pipe_diameter + 4
		mid_x = (self.tank_widget.sx + 1 + ex) / 2
		vsx = mid_x - (w / 2)
		vsy = pipe_mid_y - h / 2
		
		self.canvas.create_rectangle(vsx, vsy, vsx + w, vsy + h, outline='#b87333', fill='#b87333')
		
		self.canvas.create_rectangle(vsx+w/4, vsy, vsx + 5 + w/4, vsy - 10, outline='#b87333', fill='#b87333')
		self.canvas.create_rectangle(vsx+w*3/4, vsy, vsx - 5 + w*3/4, vsy - 10, outline='#b87333', fill='#b87333')
		
		self.canvas.create_text(mid_x, sy - 15, text='Flow DPT', fill=self.default_fg, font='Helvetica 10 bold', anchor='c')
		
		
		### INFLOW PIPE - Tank to VTube ###
		
		p = Pipe(self.tank_widget.sx+1, pipe_mid_y, self.pipe_diameter)
		p.move_left_to(vsx + w + 1)		
		self.in_pipe = self.canvas.create_polygon(p.get_points(), smooth=True, outline=self.default_fg, fill=self.default_fg)
		
		
		### INFLOW PIPE - VTube to Pump ###
		
		p = Pipe(vsx-1, pipe_mid_y, self.pipe_diameter)
		p.move_left_to(ex+1)		
		self.in_pipe2 = self.canvas.create_polygon(p.get_points(), smooth=True, outline=self.default_fg, fill=self.default_fg)
		
		
		
		### INFLOW PIPE - Pump to left wall ###
		
		p = Pipe(sx-1, pipe_mid_y, self.pipe_diameter)
		p.move_left_to(10)
		self.canvas.create_polygon(p.get_points(), smooth=True, outline=self.water_color, fill=self.water_color)
		
		
		
		
		### PUMP Dial ###
		
		d = 70
		
		x = mx - (d / 2)
		y = ey + 10
		max_val = 60.0
		
		self.pump_dial = Dial(self.canvas, sx=x, sy=y, diameter=d, step=max_val/6, text='O:1.0', bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=max_val, dead_angle=120.0)
		
		
		### VTube Dial ###
		
		mx = vsx + w / 2
		x = mx - (d / 2)
		max_val = self.tanksim.pump.max_p
		self.inflow_dial = Dial(self.canvas, sx=x, sy=y, diameter=d, step=max_val/5, text='I:0.5', bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=max_val, dead_angle=120.0)
		
		
		
		
		### OUTFLOW ###
		
		# valve rectangle params
		sx = self.tank_widget.ex + 20
		sy = self.tank_widget.ey - 40
		size = 40
		ex = sx + size
		ey = sy + size
		pipe_mid_y = ((ey + sy)/2)

		### OUTFLOW PIPE - Tank to Valve ###
		
		p = Pipe(self.tank_widget.ex-1, pipe_mid_y, self.pipe_diameter)
		p.move_right_to(sx-1)
		self.canvas.create_polygon(p.get_points(), smooth=True, outline=self.water_color, fill=self.water_color)
	
		
		### OUTFLOW PIPE - Valve to Floor ###
		
		p = Pipe(ex+1, pipe_mid_y, self.pipe_diameter)
		p.move_right(1)
		p.move_down_to(390)
		
		self.out_pipe = self.canvas.create_polygon(p.get_points(), smooth=True, outline=self.default_fg, fill=self.default_fg)
		
		
		
		
		### VALVE ###
		
		self.valve_rect = Rounded_Rect(self.canvas, sx, sy, ex, ey, radius=25, outline=self.high_color, fill=self.high_color)
	
		mx = sx + ((ex - sx) / 2)
		my = sy + ((ey - sy) / 2)
		w = 15
		h = 12
		ex = mx + w
		self.canvas.create_line(mx - w, my,  ex, my, fill=self.default_bg, width=5)
		self.canvas.create_line(ex-2, my, ex-h, my-h , fill=self.default_bg, width=5)
		self.canvas.create_line(ex-2, my, ex-h, my+h , fill=self.default_bg, width=5)
		
		self.canvas.create_text(mx, my + h + 20, text='Valve', fill=self.default_fg, font='Helvetica 10 bold', anchor='c')
		
		### Valve Dial ###
		
		d = 70
		
		x = ex + (d / 2) + 35
		y = sy
		
		self.valve_dial = Dial(self.canvas, sx=x, sy=y, diameter=d, step=20.0, text='O:1.1', bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=100.0, dead_angle=120.0)
		
		self.canvas.create_text(x+(d / 2), y - 15, text='Valve Pos', fill=self.default_fg, font='Helvetica 10 bold', anchor='c')
		
		
		##########  FloatNumpad  ##########
		
		#self.numpad = FloatNumpad(self.canvas, 'Setpoint', 'Helvetica 12 bold', (800-175-10), 10, 175, 225, bg=self.default_bg, fg=self.default_fg, default_val=20, max_val=100)
		
		
		
		##########  ButtonPanel  ##########
		
		text = 'Level SP: '
		labs = ['1,1 - 80', '1,0 - 60', '0,1 - 40', '0,0 - 20']
		vals = [80, 60, 40, 20]
		
		w = 130
		h = 170
		self.lev_butpan = ButtonPanel(self.canvas, text, labs, vals, 'Helvetica 12 bold', (800-w-25), (400-h-10), w, h, bg=self.default_bg, fg=self.default_fg, default_val=self.level_sp)
		
		self.canvas.create_text((800-w-25)+(w / 2), (400-h-10) - 15, text='SP: I:0/3,I:0/4', fill=self.default_fg, font='Helvetica 10 bold', anchor='c')
		
		
		
		text = 'Inflow SP: '
		labs = ['1,1 - 10', '1,0 - 7', '0,1 - 3', '0,0 - 0']
		vals = [10, 7, 3, 0]
		
		self.inflow_butpan = ButtonPanel(self.canvas, text, labs, vals, 'Helvetica 12 bold', 35, (400-h-10), w, h, bg=self.default_bg, fg=self.default_fg, default_val=self.default_inflow_sp)
		
		self.canvas.create_text(35+(w / 2), (400-h-10) - 15, text='SP: I:0/5,I:0/6', fill=self.default_fg, font='Helvetica 10 bold', anchor='c')
		
		
		
		
		
		
		
		
		self.canvas.pack()
		
		
	
	
	def normal_speed_clk(self):
		self.tanksim.time_scale = 1.0
	
	def double_speed_clk(self):
		self.tanksim.time_scale = 2.0
		
	def quad_speed_clk(self):
		self.tanksim.time_scale = 4.0
		
		
		
	def setup_bottom_frame(self):
		
		frame = tk.Frame(self, width=self.default_width, height=80)
		self.config_frame(frame)
		frame.grid(row = 1, column=0, columnspan=1, rowspan=1)
		
		
		self.normal_speed = tk.Button(frame, text='x1 Speed', command=self.normal_speed_clk)
		self.config_btn(self.normal_speed)
		self.normal_speed.place(relx=0.10, rely=0.5, anchor=tk.CENTER)
		
		self.double_speed = tk.Button(frame, text='x2 Speed', command=self.double_speed_clk)
		self.config_btn(self.double_speed)
		self.double_speed.place(relx=0.280, rely=0.5, anchor=tk.CENTER)
		
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

		

		
		

		

		
		



