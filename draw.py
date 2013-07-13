import pyglet
from pyglet.gl import *
from pyglet.window import key

class DiagramWindow(pyglet.window.Window):
		def __init__(self, width=800, height=800):
			super(DiagramWindow, self).__init__()

			self.width = width
			self.height = height
			self.set_size(width, height)

			self.points = []
			self.gridColor = (0, 0.2, 0.4, 1)
			self.gridWidth = []

		def on_draw(self):
			self.clear()
			self.drawGrid()
			self.drawPoints()

		def drawPoints(self):
			# Draw points by creating vertex array
			verts = []
			for point in self.points:
				verts.extend([point[0], point[1]])

			if verts:
				pyglet.gl.glColor4f(1, 0, 0, 1)
				# Draw tile as two triangles
				pyglet.graphics.draw( 
					int(len(verts)/2), 
					pyglet.gl.GL_POINTS,
					('v2f', verts)
				)

		def addPointsForDrawing(self, newPoints=[]):			
			if newPoints:
				self.points.extend(newPoints)
				print("Adding " + str(len(newPoints)) + "points to those drawn. Total: " + str(len(self.points)))
			else:
				print("List for addPointsForDrawing() contained no points: " + str(len(newPoints)))

		def addGridWidthForDrawing(self, newGridWidth):
			self.gridWidth = newGridWidth

		def drawGrid(self):
			if self.gridWidth:
				# Draw grid by creating vertex array
				gridVerts = []
				# Screen edges:
				# | west
				gridVerts.extend([0, 0, 0, self.height])
				# | north
				gridVerts.extend([0, self.height, self.width, self.height])
				# | east
				gridVerts.extend([self.width, self.height, self.width, 0])
				# | south
				gridVerts.extend([self.width, 0, 0, 0])
				# Vertical Lines
				x = self.gridWidth
				while x <= self.width:
					gridVerts.extend([x, 0, x, self.height])
					x += self.gridWidth
				# Horizontal Lines
				y = self.gridWidth
				while y <= self.height:
					gridVerts.extend([0, y, self.width, y])
					y += self.gridWidth
				# Draw
				pyglet.gl.glColor4f(*self.gridColor)
				pyglet.graphics.draw( 
					int(len(gridVerts)/2), 
					pyglet.gl.GL_LINES,
					('v2f', gridVerts)
				)

		def clearPoints(self):
			self.points = []