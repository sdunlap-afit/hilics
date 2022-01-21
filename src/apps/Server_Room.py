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




##### HVAC Components #####
## 
## Chiller - AC
## Air Handler - blower
## Air filters
## Ducts
## Damper
##		Blades in ducts to control airflow (manual or auto)
## 		Can be installed at firewalls to close during a fire
## Terminal Unit - Device with auto damper
##		Electric, pneumatic or digital actuator
##		Regulated by thermostat
## Thermostat - one per zone
## Heating coils - zone-by-zone heating
##
## https://www.youtube.com/watch?v=-v0wgRyJ8tk
##


try:
	import Tkinter as tk
	from Tkinter import ttk
	from Tkinter.font import Font
except ImportError:
	import tkinter as tk
	from tkinter import ttk
	from tkinter.font import Font

from PIL import ImageTk, Image

##### Create a new sim using BlankSim as a template and update the import here

from sims.ServerSim import ServerSim

from widgets.Dial import Dial
from widgets.RoundRectangle import round_rectangle
from widgets.Graph import Graph
from widgets.ButtonPanel import ButtonPanel

import threading
import time
import math



class Server_Room(tk.Frame):
	
	
	
	def __init__(self, master=None, default_bg=None, default_fg=None):
		self.master = master

		##### You can change the color scheme here

		self.default_bg = default_bg
		self.default_fg = default_fg
		
		self.high_color = '#EC7600'
		self.low_color = '#678CB1'
		
		

		##### Update this line with your Sim class

		self.sim = ServerSim()
		self.val = 0.0

		self.last_graph_update = 0.0

		
		super().__init__(master)
		self.pack()

		##### create_widgets is the entry point for setting up the GUI

		self.create_widgets()
	

		##### worker_thread handles updating the simulation and any display items

		self.running = True
		self.thread = threading.Thread(target=self.worker_thread)
		self.thread.setDaemon(True)
		self.thread.start()
		
		
	
	##### This function is called when the App is closing
	
	def clean_up(self):
		self.running = False
		self.thread.join(1.0)
		self.sim.close()
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
	
	



	def update_graph(self):
		t = time.time()
		
		if t - self.last_graph_update > 1.0:
			self.last_graph_update = t
			self.graph.add_point(0, self.sim.building.temp_f)
			self.graph.add_point(1, self.sim.server_room.temp_f)
			self.graph.add_point(2, 3.0)
			self.graph.add_point(3, 4.0)


	def update_servers(self):
		for i, server in enumerate(self.sim.servers):
			if server.status == server.RUNNING:
				self.canvas.itemconfig(self.servers_text[i], text="Running")
				self.canvas.itemconfig(self.servers_text[i], fill='#005000')
			elif server.status == server.THROTTLED:
				self.canvas.itemconfig(self.servers_text[i], text="Throttled")
				self.canvas.itemconfig(self.servers_text[i], fill='#505000')
			elif server.status == server.SHUTDOWN:
				self.canvas.itemconfig(self.servers_text[i], text="Shutdown")
				self.canvas.itemconfig(self.servers_text[i], fill='#500000')
			else:
				self.canvas.itemconfig(self.servers_text[i], text="Sim Error")
				self.canvas.itemconfig(self.servers_text[i], fill='#FF0000')
				


	##### worker_thread handles updating the simulation and any display items
	
	def worker_thread(self):
	
		while self.running:
		
			try:
				
				self.sim.server_rm_ac_percent = self.ac_butpan.val

				##### Update the simulation
				self.sim.update()

				self.update_servers()


				##### Update display items here

				self.update_graph()

				self.graph.bring_to_top()

				self.building_temp_dial.update(self.sim.building.temp_f)
				self.server_room_temp_dial.update(self.sim.server_room.temp_f)

				##### Choose an appropriate sleep duration (smaller value for faster processes)
				time.sleep(0.1)
			
			except Exception as e: 
				print(e)
		
	

	### Create a basic representation of a server rack with the
	### top left corner positioned at (x, y) 
	def create_server_rack(self, canvas, x, y, width, height, rows=7, columns=2):
		
		padding = 5

		round_rectangle(canvas, x, y, x+width, y+height, radius=10, outline=self.default_fg, fill=self.default_fg)
		
		canvas.create_text(x + int(width/2), y+2*padding, anchor='c', text = 'Servers', font=("Helvetica", 14), fill=self.default_bg)

		y += 14
		height -= 14
		col_width = int((width - (padding * (columns + 1))) / columns)
		row_height = int((height - (padding * (rows + 1))) / rows)
		

		self.servers_text = []

		for c in range(columns):
			
			sx = x + c * col_width + (c+1) * padding
			ex = sx + col_width

			for r in range(rows):
				sy = y + r * row_height + (r+1) * padding
				ey = sy + row_height
				
				round_rectangle(canvas, sx, sy, ex, ey, radius=10, outline=self.default_bg, fill=self.default_bg)
				
				h = int(row_height * 0.5) / 2
				w = int(h * 4)

				ind_x = int(sx + col_width * 0.3)
				ind_y = int(sy + row_height / 2)
				
				canvas.create_rectangle(ind_x-w, ind_y-h, ind_x + w, ind_y + h, outline=self.default_fg, fill=self.default_fg)
				
				txt = canvas.create_text(ind_x, ind_y, anchor='c', text = 'Running', font=("Helvetica", 10), fill='#00FF00')
				
				self.servers_text.append(txt)

				ind_x = int(sx + col_width * 0.65)
				r = int(row_height * 0.3) / 2


				canvas.create_oval(ind_x-r, ind_y-r, ind_x+r, ind_y+r, outline='#008000', fill='#008000')
				ind_x += 2*r + 5
				canvas.create_oval(ind_x-r, ind_y-r, ind_x+r, ind_y+r, outline='#800000', fill='#800000')
				ind_x += 2*r + 5
				canvas.create_oval(ind_x-r, ind_y-r, ind_x+r, ind_y+r, outline='#000080', fill='#000080')
	
	
	##### These setup methods create the frames for your App
	#
	# Frame1 is the primary display and is 800 pixels wide by 400 pixels tall (leaving 80 pixels for the bottom panel)
	# You can split this frame into columns and rows like IO_Test
	# Or you can create a canvas to fill the frame and do all your work in that (like GarageDoor)
	# 
	# I recommend using a canvas
	
	def setup_main_frame(self):
		
		frame = tk.Frame(self, width=800, height=400)
		self.config_frame(frame)
		frame.grid(row = 0, column=0, columnspan=2, rowspan=1)		
		
		self.canvas = tk.Canvas(frame, width=800, height=400, bd=0, highlightthickness=0, relief='ridge')
		self.config_bg(self.canvas)


		##### AC ButtonPanel #####

		text = 'Server Rm AC: '
		labs = ['100 %', '66 %', '33 %', '0 %']
		vals = [100, 66, 33, 0]
		
		w = 130
		h = 100
		self.ac_butpan = ButtonPanel(self.canvas, text, labs, vals, 'Helvetica 12 bold', 10, 10, w, h, bg=self.default_bg, fg=self.default_fg, default_val=100)



		##### Server Rack #####

		x = 10
		y = 150
		self.create_server_rack(self.canvas, x, y, 300, 400 - y - 10)	

		##### Sensor Dials #####

		d = 70
		gap = 10
		max_val = 150.0
		font = ("Helvetica", 8)

		x, y = 330, 20

		self.canvas.create_text((x + d + gap / 2), y - gap, text='Sensors', font=("Helvetica", 12), fill=self.default_fg, anchor='c')
		
		self.building_temp_dial = Dial(self.canvas, sx=x, sy=y, diameter=d, step=max_val/10, text='Bldg (°F)', text_font=font, bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=max_val, dead_angle=120.0)
		self.server_room_temp_dial = Dial(self.canvas, sx=(x + d + gap), sy=y, diameter=d, step=max_val/10, text='Srv Rm (°F)', text_font=font, bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=max_val, dead_angle=120.0)

		
		##### Actuator Dials #####

		max_val = 100
		x = x + 2*d + 3*gap
		
		font = ("Helvetica", 9)
		self.canvas.create_text((x + d + gap / 2), y - gap, text='Actuators', font=("Helvetica", 14), fill=self.default_fg, anchor='c')
		
		self.damper_dial = Dial(self.canvas, sx=x, sy=y, diameter=d, step=max_val/10, text='Damper', text_font=font, bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=max_val, dead_angle=120.0)
		self.reheat_dial = Dial(self.canvas, sx=(x + d + gap), sy=y, diameter=d, step=max_val/10, text='Reheat', text_font=font, bg=self.default_bg, fg=self.default_fg, minval=0.0, maxval=max_val, dead_angle=120.0)


		##### Fan Speed Indicator #####


		font = ("Helvetica", 9)
		self.canvas.create_text((x + d + gap / 2), y - gap, text='Actuators', font=("Helvetica", 14), fill=self.default_fg, anchor='c')

		ht = 125
		wd = 75
		sx = x + 2*d + 3*gap
		sy = y - 10
		ex = sx + wd
		ey = sy + ht
		
		#rect = self.canvas.create_rectangle(sx, sy, ex, ey, outline=self.default_fg, fill=self.default_fg)
		round_rectangle(self.canvas, sx, sy, ex, ey, radius=25, outline=self.default_fg, fill=self.default_fg)
				
		
		x = sx + ((ex - sx) / 2)
		y = sy + 15
		self.canvas.create_text(x, y, anchor='c', text = 'Fan Speed', font=("Helvetica", 14), fill=self.default_bg)
				
		r = 15

		font = ("Helvetica", 10)
		
		x = sx + ((ex - sx) / 4)
		y = sy + 10 + (1 * (ey - sy) / 4)
		self.fan__ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'HIGH', font=font, fill=self.default_bg)
		
		x = sx + ((ex - sx) / 4)
		y = sy + 10 + (2 * (ey - sy) / 4)
		self.fan_med_ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'MED', font=font, fill=self.default_bg)
		
		x = sx + ((ex - sx) / 4)
		y = sy + 10 + (3 * (ey - sy) / 4)
		self.fan_high_ind = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.default_fg, fill=self.low_color)
		
		self.canvas.create_text(x + r + 2, y, anchor='w', text = 'LOW', font=font, fill=self.default_bg)
		

		##########  Graph  ##########
		
		w = 340
		h = 170
		self.graph = Graph(self.canvas, 800-w-25, 200, w, h, self.default_fg, self.default_bg, 130, 100, lines=True)
		self.graph.add_graph('#0000C0', 'Building °F', ("Helvetica", 8))
		self.graph.add_graph('#00C000', 'Server Room °F', ("Helvetica", 8))
		self.graph.add_graph('#C00000', 'UPDATE ME', ("Helvetica", 8))
		self.graph.add_graph('#505050', 'UPDATE ME', ("Helvetica", 8))



		self.canvas.pack()
		


	##### The two bottom frames are for any config buttons and the Back button.
	# You can also add images or labels

	def normal_speed_clk(self):
		self.sim.time_scale = 1.0
	
	def double_speed_clk(self):
		self.sim.time_scale = 2.0
		
	def quad_speed_clk(self):
		self.sim.time_scale = 100.0
		
		
		
	def setup_bottom_frame(self):
		
		frame = tk.Frame(self, width=800, height=80)
		self.config_frame(frame)
		frame.grid(row = 1, column=0, columnspan=1, rowspan=1)
		
		
		self.normal_speed = tk.Button(frame, text='x1 Speed', command=self.normal_speed_clk)
		self.config_btn(self.normal_speed)
		self.normal_speed['width'] = 7
		self.normal_speed.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
		
		self.double_speed = tk.Button(frame, text='x2 Speed', command=self.double_speed_clk)
		self.config_btn(self.double_speed)
		self.double_speed['width'] = 7
		self.double_speed.place(relx=0.22, rely=0.5, anchor=tk.CENTER)

		self.quad_speed = tk.Button(frame, text='x100 Speed', command=self.quad_speed_clk)
		self.config_btn(self.quad_speed)
		self.quad_speed['width'] = 7
		self.quad_speed.place(relx=0.34, rely=0.5, anchor=tk.CENTER)

		
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
		
		
	


	##### If you add any methods for setting up frames, call them here

		
	def create_widgets(self):
	
		self.master.minsize(width=800, height=480)
		self.master.maxsize(width=800, height=480)


		self.setup_main_frame()
		
		self.setup_bottom_frame()

		

		
		

		

		
		

		


