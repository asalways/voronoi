import math
import random

import pyglet

class Point():
	def __init__(self, x, y):
		if x < 0:
			x = 0
		if x > 800:
			x = 800
		
		if y < 0:
			y = 0
		if y > 800:
			y = 800
		
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
