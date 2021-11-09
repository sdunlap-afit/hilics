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





#####----- Instructions -----#####
#
# This is a simple template to get started making your own simulation for HILICS
# To create your own App:
#	1. Create a copy of apps/BlankApp.py in the apps directory and name it appropriately
#	2. Rename the BlankApp class to match the new filename (must match exactly for import to work)
#	3. Create a copy of sims/BlankSim.py and name it appropriately
#	4. Rename the BlankSim class
#	5. Update the import statement below to reference your new Sim instead of BlankSim
#	6. Add your App to apps/appsList.txt (this will add it to the main display)
#		If you have more than 6 apps, the rest will be shown in the drop-down menu



try:
	import Tkinter as tk
	from Tkinter import ttk
	from Tkinter.font import Font
except ImportError:
	import tkinter as tk
	from tkinter import ttk
	from tkinter.font import Font


##### Create a new sim using BlankSim as a template and update the import here

from sims.ServerSim import ServerSim


from widgets.Dial_Canvas import Dial_Canvas
from widgets.FloatNumpad import FloatNumpad
from widgets.Tank import Tank


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
	
	
	

	##### worker_thread handles updating the simulation and any display items
	
	def worker_thread(self):
	
		while self.running:
		
			try:
				
				##### Update the simulation
				self.sim.update()



				##### Update display items here



				##### Choose an appropriate sleep duration (smaller value for faster processes)
				time.sleep(0.01)
			
			except Exception as e: 
				print(e)
		
		
		
	
	
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
		

		
		self.canvas.pack()
		


	##### The two bottom frames are for any config buttons and the Back button.
	# You can also add images or labels


	
	def setup_bottom_left_frame(self):
		
		frame = tk.Frame(self, width=400, height=80)
		self.config_frame(frame)
		frame.grid(row = 1, column=0, columnspan=1, rowspan=1)
		
		
		
		
	def setup_bottom_right_frame(self):
		
		frame = tk.Frame(self, width=400, height=80)
		self.config_frame(frame)
		frame.grid(row = 1, column=1, columnspan=1, rowspan=1)
		
		
		self.quit = tk.Button(frame, text='Back', command=self.clean_up)
		self.config_btn(self.quit)
		self.quit.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
		
		
	


	##### If you add any methods for setting up frames, call them here

		
	def create_widgets(self):
	
		self.master.minsize(width=800, height=480)
		self.master.maxsize(width=800, height=480)


		self.setup_main_frame()
		
		self.setup_bottom_left_frame()
		self.setup_bottom_right_frame()

		

		
		

		

		
		

		


