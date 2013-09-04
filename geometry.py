import math
import random

import pyglet

class Point():
	def __init__(self, x, y):
		self.id = next(pointIdGen)
		self.coords = [x, y]
		self.altitude = random.random()

	def drawPoint(self, color=False):
		if color:
			pyglet.gl.glColor4f(*color)
		pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
			('v2f', self.coords)
		)


class Cell():
	def __init__(self, centre, points):
		self.id = next(cellIdGen)		
		self.centre = centre
		self.trueCentre = centre
		self.points = points
		self.color = (random.random(), random.random(), random.random(), 0.1)
		self.selected = False

	def drawFilledCell(self, color=False):
		#print("Drawing a cell")
		# Iterate over points, drawing triangles
		if color:
			pyglet.gl.glColor4f(*color)
		else:
			pyglet.gl.glColor4f(*self.color)
		verts = []
		if len(self.points) > 2:
			for i in range(len(self.points)):
				verts.extend( self.points[i].coords )
				verts.extend( self.points[i-1].coords )
				verts.extend( self.trueCentre.coords )
				#print(self.trueCentre.coords)
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

	def toggleSelection(self):
		# Turn opacity up or down
		self.selected = not self.selected
		if self.selected:
			self.color = (self.color[0], self.color[1], self.color[2], 1)
		else:
			self.color = (self.color[0], self.color[1], self.color[2], 0.1)

def idGenerator():
	i = 0
	while True:
		yield i
		i += 1

# Initialise the generator
cellIdGen = idGenerator()
pointIdGen = idGenerator()
