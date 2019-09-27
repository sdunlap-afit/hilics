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
from widgets.GraphPoint import GraphPoint
import time


class Graph():
	
	
	def __init__(self, canvas, x, y, width, height, bg, fg, max_y, time_range, lines=False, parent=None):
		self.canvas = canvas
		
		self.lines = lines
		
		self.is_top = False
		
		self.sx = x
		self.sy = y
		self.ex = x + width
		self.ey = y + height
		self.width = width
		self.height = height
		if parent is None:
			self.radius = (height + width) / 16
		else:
			self.radius = (height + width) / 32
		
		self.padding = 20
		
		self.chart_sx = self.sx + self.padding
		self.chart_sy = self.sy + self.padding
		self.chart_ex = self.ex - self.padding
		self.chart_ey = self.ey - self.padding
		
		
		self.bg = bg
		self.fg = fg
	
		self.font = ("Helvetica", 5)
		
		self.step = 10

		self.parent = parent
		self.fullscreenGraph = None
		
		self.max_y_val = max_y
		
		self.staticElements = []

		# in seconds
		self.time_range = time_range
		
		self.colors = []
		self.legends = []
		self.fonts = []
		self.graphs = []
		
		self.last_time = 0
		
		self.create_frame()
		self.create_x_axis()
		self.create_y_axis()
		

	def is_full(self):
		return not self.fullscreenGraph is None
		
		
	def resize(self):
		if not self.parent:
			print("Creating fullscreen Graph")
			self.fullscreenGraph = Graph(self.canvas, 10, 10, 780, 380, self.bg, self.fg, self.max_y_val, self.time_range, lines=self.lines, parent=self)
			
			
			for i in range(len(self.fonts)):
				self.fullscreenGraph.add_graph(self.colors[i], self.legends[i], self.fonts[i])
				
			
			self.fullscreenGraph.graphs = self.graphs
			self.fullscreenGraph.last_time = self.last_time
			#self.fullscreenGraph.colors  = self.colors  
			#self.fullscreenGraph.legends  = self.legends
			#self.fullscreenGraph.fonts  = self.fonts
		
			#i = 0
			#for line in self.graphs:
			#	for point in line:
			#		#print("Point: " + str(point.x) + " : " + str(point.y) + " : ")
			#		self.fullscreenGraph.add_point(i, point.y, t=point.x)
			#	#print("Done with index: " + str(i))
			#	i = i + 1
			#self.bring_to_top()
			print("Done creating graph.")
		else:
			print("Destroying fullscreen self.")
			self.destroy()


	def create_frame(self):
		self.frame = Rounded_Rect(self.canvas, self.sx, self.sy, self.ex, self.ey, radius=self.radius, outline=self.bg, fill=self.bg)
		self.canvas.tag_bind(self.frame.id, '<Button-1>', lambda e: self.resize())
		
		
	def create_x_axis(self):
		y = self.chart_ey + 4
		
		mainLine = self.canvas.create_line(self.chart_sx, y, self.chart_ex, y, fill=self.fg, width=2)
		self.staticElements.append(mainLine)

		for i in range(0, self.time_range + 5, self.step):
			x = self.val_to_x(i)
			line = self.canvas.create_line(x, y, x, y-3, fill=self.fg, width=2)
			self.staticElements.append(line)
			text = self.canvas.create_text(x, y+5, anchor='c', text=str(-i), fill=self.fg, font=self.font)
			self.staticElements.append(text)
		
		
		
	def create_y_axis(self):
		x = self.chart_sx - 4
		
		mainLine = self.canvas.create_line(x, self.chart_sy, x, self.chart_ey, fill=self.fg, width=2)
		self.staticElements.append(mainLine)

		for i in range(0, self.max_y_val + 5, self.step):
			y = self.val_to_y(i)
			line = self.canvas.create_line(x, y, x+3, y, fill=self.fg, width=2)
			self.staticElements.append(line)
			text = self.canvas.create_text(x-3, y, anchor='e', text=str(i), fill=self.fg, font=self.font)
			self.staticElements.append(text)


	
	def val_to_x(self, x):
		return int(self.chart_ex - ((self.chart_ex - self.chart_sx) * x / self.time_range))

		
		
	def val_to_y(self, y):
		return int(self.chart_ey - ((self.chart_ey - self.chart_sy) * y / self.max_y_val))


	def bring_to_top(self):
	
		if not self.fullscreenGraph is None:
			if not self.fullscreenGraph.is_top:
				self.fullscreenGraph.is_top = True

				self.fullscreenGraph.frame.bring_to_top()
				for element in self.fullscreenGraph.staticElements:
					self.fullscreenGraph.canvas.tag_raise(element)
				for graph in self.fullscreenGraph.graphs:
					for point in graph:
						self.fullscreenGraph.canvas.tag_raise(point.line)


	def destroy(self):
		self.parent.fullscreenGraph = None

		for element in self.staticElements:
			self.canvas.delete(element)
		#for graph in self.graphs:
		#	for point in graph:
		#		self.canvas.delete(point.line)
		
		self.frame.cleanUp()
		self.frame = None



	def add_graph(self, color, legend='', font=None):
		self.colors.append(color)
		self.legends.append(legend)
		self.fonts.append(font)
		self.graphs.append([])
		
		if len(legend) > 0:
		
			if font is None:
				font = self.font
				
			ht = font[1] + font[1] / 2
			
			num = len(self.graphs)
			y = self.sy + (num * ht)
			text = self.canvas.create_text(self.ex-3, y, anchor='e', text=legend, fill=color, font=font)
			self.staticElements.append(text)
		
		
	
	def shift_times(self, time_dif):
		for graph in self.graphs:
			for point in graph:
				point.x += time_dif
			
			while len(graph) > 0 and graph[0].x > self.time_range:
				self.canvas.delete(graph[0].line)
				graph.pop(0)
			
				self.canvas.itemconfig(graph[0].line, state='hidden')
				#Why hide the line when you can just delete it?
				#self.canvas.delete(graph[0].line)
		
		
		
		
	def add_point(self, index, val, t = None):

		#If we has a fullscreen graph we need to add points.
		if not self.fullscreenGraph is None:
		
			self.fullscreenGraph.add_point(index, val)
			
			
		else:
		
			if t is None:
				t = time.time()
				
				if self.last_time == 0:
					self.last_time = t
				
				
				time_dif = t - self.last_time
				self.last_time = t
				
			else:
				time_dif = t
			
			self.shift_times(time_dif)
			
			line = self.canvas.create_line(0, 0, 1, 1, fill=self.colors[index], width=1)
			point = GraphPoint(0, val, line)
			self.graphs[index].append(point)
			
			if len(self.graphs[index]) == 1:
				self.canvas.itemconfig(line, state='hidden')
			
			for graph in self.graphs:
				if self.lines:
					
					for i in range(1, len(graph)):
						x1 = self.val_to_x(graph[i].x)
						y1 = self.val_to_y(graph[i].y)
						x2 = self.val_to_x(graph[i-1].x)
						y2 = self.val_to_y(graph[i-1].y)
						line = graph[i].line
						
						self.canvas.coords(line, x1, y1, x2, y2)
			
				else:
				
					for point in graph:
						x = self.val_to_x(point.x)
						y = self.val_to_y(point.y)
						line = point.line
			
						self.canvas.coords(line, x, y, x+2, y)
		
		
		
		
		
	
