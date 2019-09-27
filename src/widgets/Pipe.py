#!/usr/bin/env python
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


START = 0
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
CORNER = 5


class Pipe:


	def __init__(self, x, y, d):
		
		self.sx = x
		self.sy = y
			
		self.d = d
		self.radius = d + (d / 2)
		
		self.last_move = START
		
		self.start_points = []
		self.end_points = []
		
	
	def get_points(self):
		return self.start_points + self.end_points
		
	
	def check_first_move(self, move):
		# If first move:
		if self.last_move == START:
		
			# If horizontal, then add y points
			if move == LEFT or move == RIGHT:	
				self.ey = self.sy - (self.d / 2)
				self.sy = self.sy + (self.d / 2)
				self.ex = self.sx
				
			elif move == UP or move == DOWN:	
				self.ex = self.sx - (self.d / 2)
				self.sx = self.sx + (self.d / 2)
				self.ey = self.sy
		
			self.save_point(START)
	
	
	def print_points(self):
		print(self.start_points) 
		print(self.end_points)
		print()
	
	
	def save_point(self, move):
	
		# Append start points
		self.start_points += [self.sx, self.sy]
		self.start_points += [self.sx, self.sy]
		
		# Prepend end points
		self.end_points = [self.ex, self.ey] + self.end_points
		self.end_points = [self.ex, self.ey] + self.end_points
		
		if not move == CORNER and not move == START:
			self.last_move = move
		
		
		
		
	def move_left(self, dist):
	
		self.check_first_move(LEFT)
		self.corner(LEFT)
	
		self.sx -= dist
		self.ex -= dist
		self.save_point(LEFT)
		
		
	def move_right(self, dist):
	
		self.check_first_move(RIGHT)
		self.corner(RIGHT)
		
		self.sx += dist
		self.ex += dist
		self.save_point(RIGHT)
		
		
		
	def move_up(self, dist):

		self.check_first_move(UP)
		self.corner(UP)
			
		self.sy -= dist
		self.ey -= dist
		self.save_point(UP)
		
		
		
	def move_down(self, dist):
	
		self.check_first_move(DOWN)
		self.corner(DOWN)
		
		self.sy += dist
		self.ey += dist
		self.save_point(DOWN)
	
	
	
	
	def move_left_to(self, x):
	
		self.check_first_move(LEFT)
		self.corner(LEFT)
	
		self.sx = x
		self.ex = x
		self.save_point(LEFT)
		
		
	def move_right_to(self, x):
	
		self.check_first_move(RIGHT)
		self.corner(RIGHT)
		
		self.sx = x
		self.ex = x
		self.save_point(RIGHT)
		
		
		
	def move_up_to(self, y):

		self.check_first_move(UP)
		self.corner(UP)
			
		self.sy = y
		self.ey = y
		self.save_point(UP)
		
		
		
	def move_down_to(self, y):
	
		self.check_first_move(DOWN)
		self.corner(DOWN)
		
		self.sy = y
		self.ey = y
		self.save_point(DOWN)
		
		
		
		
		
	
	def is_horizontal(self, move):	
		return (move == LEFT or move == RIGHT)
	
	def is_vertical(self, move):	
		return (move == UP or move == DOWN)
	
	
	
	
	
	def corner(self, move):	
		if self.last_move == START or self.last_move == CORNER:
			return

		xf = (self.last_move == LEFT or self.last_move == RIGHT)
		dn = (self.last_move == DOWN or move == DOWN)
		lt = (self.last_move == LEFT or move == LEFT)
		

		
		if self.is_horizontal(self.last_move):
			# Add to x if moving right
			xd = self.d
			if self.last_move == LEFT:
				# Subtract from x if moving left
				xd = 0 - xd
				
			if move == UP:
				if self.sy > self.ey:
					self.sx += xd
				else:
					self.ex += xd
			
			else:
				if self.sy < self.ey:
					self.sx += xd
				else:
					self.ex += xd
			
			self.save_point(CORNER)
		
		
		
		elif self.is_vertical(self.last_move):
			# Add to x if moving right
			xy = self.d
			if self.last_move == UP:
				# Subtract from x if moving left
				xy = 0 - xy
				
			if move == RIGHT:
				if self.sx < self.ex:
					self.sy += xy					
				else:
					self.ey += xy
			else:
				if self.sx > self.ex:
					self.sy += xy					
				else:
					self.ey += xy
			
				self.save_point(CORNER)
		
		
		self.sx, self.sy, points = self.single_corner(self.sx, self.sy, xfirst=xf, down=dn, left=lt)
		self.start_points += points
		
		self.ex, self.ey, points = self.single_corner(self.ex, self.ey, xfirst=xf, down=dn, left=lt)
		self.end_points = points + self.end_points
		
		self.save_point(CORNER)
		
		if move == UP:
			self.sy = min(self.sy, self.ey)
			self.ey = self.sy
		elif move == DOWN:
			self.sy = max(self.sy, self.ey)
			self.ey = self.sy
			
		elif move == LEFT:
			self.sx = min(self.sx, self.ex)
			self.ex = self.sx
		elif move == RIGHT:
			self.sx = max(self.sy, self.ex)
			self.ex = self.sx
		
		self.save_point(CORNER)
		
		
		
		
	
		
	
	
	
	def single_corner(self, x, y, xfirst=True, down=True, left=True):
		
		# diameter is always positive
		xd = self.radius
		yd = self.radius
		
		# Invert the direction if necessary
		if left:
			xd = 0 - xd
			
		if not down:
			yd = 0 - yd
			
		# Do first axis
		if xfirst:
			x += xd
			points = [x, y]
			y += yd
		else:
			y += yd
			points = [x, y]				
			x += xd
		
		return x, y, points
		
		
		
		







































		
		
		
		
		
	