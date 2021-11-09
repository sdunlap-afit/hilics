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

import os
import sys
import time
import importlib


from PIL import ImageTk
from PIL import Image




class Main(tk.Frame):

	def __init__(self, master=None):

		self.app = None

		##### These colors apply to the main display and all Apps (unless ignored)

		self.default_bg = '#293B34'
		self.default_fg = '#E0E2E4'
		
		self.master = master
		super().__init__(master)
		self.pack()
		self.create_widgets()




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
		btn['width'] = 10
		btn['height'] = 2
		
		btn['activebackground'] = self.default_bg
		btn['activeforeground'] = self.default_fg
		
		btn['bd'] = 0
		btn['highlightthickness'] = 1
		btn['relief'] = 'ridge'
		
		self.config_bg(btn)
		self.config_fg(btn)
	


	def config_optionMenu(self, mnu):
		mnu['font'] = Font(root=self.master, family='Helvetica', size=18)
		mnu['width'] = 10
		mnu['height'] = 2
		mnu['activebackground'] = self.default_bg
		mnu['activeforeground'] = self.default_fg
		
		mnu['bd'] = 0
		mnu['highlightthickness'] = 1
		mnu['relief'] = 'ridge'

		mnu['menu'].config(font=Font(root=self.master, family='Helvetica', size=18))
		mnu['menu'].config(activebackground=self.default_bg)
		mnu['menu'].config(activeforeground=self.default_fg)

		self.config_bg(mnu)
		self.config_fg(mnu)



	def config_label(self, lab):
		lab['font'] = Font(root=self.master, family='Helvetica', size=18)
		lab['width'] = 10
		lab['height'] = 2

		self.config_bg(lab)
		self.config_fg(lab)
		
	

	##### These methods handle loading and launching apps from apps/appsList.txt

	def launch_app(self, App):
		if self.app is None or self.app.running == False:
			r = tk.Toplevel()
			r.wm_attributes('-fullscreen', True)
			self.app = App(master=r, default_bg=self.default_bg, default_fg=self.default_fg)

		

	def chooseApp(self, value):
		if value is not "Select":
			mod = importlib.import_module("apps."+value)
			self.launch_app(getattr(mod, value))



	def getAppsList(self):
		listOfApps = []
		with open("./apps/appsList.txt") as appsList:
			for line in appsList:
				listOfApps.append(line.strip())
		return listOfApps



	def setup_top_frame(self):
		frame = tk.Frame(self, width=800, height=400)
		self.config_frame(frame)

		frame.grid(row = 0, column=0, columnspan=2, rowspan=1)
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_columnconfigure(2, weight=1)


		appList = self.getAppsList()
		rowNum = 1
		columnNum = 0
		appIndex = 0
		optionList = []
		optionList.append("Select")
		
		##### Create button for each app listed in apps/appsList.txt

		for app in appList:
			if appIndex < 6:
				#print("Adding button: " + appList[appIndex])

				b = tk.Button(frame, text=appList[appIndex], command=lambda j=appIndex:self.chooseApp(appList[j]))
				self.config_btn(b)
				b.grid(column=columnNum, row=rowNum, pady=20)
			else:
				optionList.append(app)
			appIndex += 1
			rowNum += 1
			if rowNum == 4:
				rowNum = 1
				columnNum += 1


		##### Drop-down menu in case more than 6 apps are listed
		
		self.dropVar = tk.StringVar()
		self.dropVar.set(optionList[0]) #Default choice
		dropMenu = tk.OptionMenu(frame, self.dropVar, *optionList, command=self.chooseApp)
		self.config_optionMenu(dropMenu)
		dropMenu.grid(column=2, row=1, pady=20)

		ccr_size = 180
		self.ccrCanvas = tk.Canvas(frame, bg=self.default_bg, width=ccr_size,height=ccr_size, bd=0, highlightthickness=0, relief='ridge')
		self.ccrCanvas.grid(column=2, row=2, rowspan=2)
		img = Image.open('./images/ccr_logo.png').resize((ccr_size, ccr_size), Image.ANTIALIAS)
		self.ccrImage = ImageTk.PhotoImage(img)
		self.ccrCanvas.create_image(0,0,image=self.ccrImage,anchor="nw")
	
	
	def setup_bottom_left_frame(self):
		
		frame = tk.Frame(self, width=400, height=80)
		self.config_frame(frame)
		
		frame.grid(row = 1, column=0, columnspan=1, rowspan=1)
		

	def setup_bottom_right_frame(self):
		
		frame = tk.Frame(self, width=400, height=80)
		self.config_frame(frame)
		
		frame.grid(row = 1, column=1, columnspan=1, rowspan=1)
		
		self.logoCanvas = tk.Canvas(frame, bg=self.default_bg, width=180,height=77, bd=0, highlightthickness=0, relief='ridge')
		self.logoCanvas.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
		self.logoImage = ImageTk.PhotoImage(file='./images/afit_logo.png')
		self.logoCanvas.create_image(0,0,image=self.logoImage,anchor="nw")

		self.quit = tk.Button(frame, text='Exit', command=self.master.destroy)
		self.config_btn(self.quit)
		self.quit.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

		
		
	def create_widgets(self):
	
		self.master.minsize(width=800, height=480)
		self.master.maxsize(width=800, height=480)

		self.setup_top_frame()
		self.setup_bottom_left_frame()
		self.setup_bottom_right_frame()

		
		
if __name__ == '__main__':

	root = tk.Tk()
	root.wm_attributes('-fullscreen', True)
	app = Main(master=root)
	app.mainloop()

