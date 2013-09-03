import math
import random

import pyglet

class Point():
	def __init__(self, x, y, xInterval, yInterval):
		# if x < xInterval[0]:
		# 	x = xInterval[0]
		# if x > xInterval[1]:
		# 	x = xInterval[1]
		
		# if y < yInterval[0]:
		# 	y = yInterval[0]
		# if y > yInterval[1]:
		# 	y = yInterval[1]
		
		self.coords = [x, y]
		self.altitude = random.random()

class Cell():
	def __init__(self, centre, points):
		self.centre = centre
		self.points = points
		self.color = (random.random(), random.random(), random.random(), 0.2)

	def drawFilledCell(self):
		# Iterate over points, drawing triangles
		pyglet.gl.glColor4f(*self.color)
		verts = []
		if len(self.points) > 2:
			for i in range(len(self.points)):
				verts.extend( self.points[i].coords )
				verts.extend( self.points[i-1].coords )
				verts.extend( self.centre.coords )
				#print(self.centre.coords)
		#print(verts)
		pyglet.graphics.draw(len(verts)/2, pyglet.gl.GL_TRIANGLES,
			('v2f', verts)
		)

	def drawCellBorder(self):
		pyglet.gl.glColor4f(1,0,0,1)
		verts = []
		for point in self.points:
			verts.extend(point.coords)
		pyglet.graphics.draw(len(verts)/2, pyglet.gl.GL_LINE_LOOP,
			('v2f', verts)
		)
