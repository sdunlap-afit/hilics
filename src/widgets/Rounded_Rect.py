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
	


class Rounded_Rect():
	
	
	def __init__(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
		self.canvas = canvas
		
		self.coords = [x1, y1, x2, y2]
		self.radius = radius
		
	
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

		self.poly = self.canvas.create_polygon(points, kwargs, smooth=True)
		self.id = self.poly

	def bring_to_top(self):
		self.canvas.tag_raise(self.poly)

	def cleanUp(self):
		self.canvas.delete(self.poly)
		































