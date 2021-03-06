import math
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import Window

from pyglet.window import mouse

import geometry

class DiagramWindow(pyglet.window.Window):
		def __init__(self, width=800, height=800, xInterval=0, yInterval=0):
			super(DiagramWindow, self).__init__()

			self.width = width
			self.height = height
			self.xInterval = xInterval
			self.yInterval = yInterval
			self.set_size(width, height)

			self.points = []
			self.gridColor = (0, 0.2, 0.4, 1)
			self.gridWidth = []

			self.vertices = []
			self.ridgePoints = []
			self.ridgeVertices = []
			self.regions = []

			self.pointObjs = []
			self.cellObjs = []

			self.mouseX = self.width/2
			self.mouseY = self.height/2

			self.hoveredCell = None

		#@Window.event
		def on_mouse_press(self, x, y, button, modifiers):
			if button == mouse.LEFT:
				self.hoveredCell.toggleSelection()

		def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
			self.mouseX = x
			self.mouseY = y
			if button == mouse.LEFT:
				# If selection has changed, toggle selection for new cell
				if self.findHoveredCell():
					self.hoveredCell.toggleSelection()

		#@Window.event
		def on_mouse_motion(self, x, y, dx, dy):
			self.mouseX = x
			self.mouseY = y
			self.findHoveredCell()

		def on_draw(self):
			self.clear()
			self.drawGrid()
			#self.drawPoints(self.points, (1,0,0,1))
			#self.drawPoints(self.vertices, (1,0,1,1))
			#self.drawRegions()
			#self.drawRidgePoints()
			#self.drawRidgeVertices()
			
			self.drawFilledCells()
			self.drawCellObjBorders()
			self.highlightHoveredCell()
			#self.drawCellObjTrueCentres()
			self.drawHoverCellVoronoiCentre()
			self.drawAreaLimit()

		def drawPoints(self, points, col):
			# Draw points by creating vertex array
			verts = []
			for point in points:
				verts.extend( point )

			if verts:
				pyglet.gl.glColor4f(*col)
				# Draw tile as two triangles
				pyglet.graphics.draw( 
					int(len(verts)/2), 
					pyglet.gl.GL_POINTS,
					('v2f', verts)
				)
		
		def drawRegions(self):
			pyglet.gl.glColor4f(1,1,1,1)
			for region in self.regions:
				verts = []
				#print(region)
				for pointIndex in region:
					#print("Vertices length: " + str(len(self.vertices)))
					#print(self.vertices[pointIndex])
					verts.extend( self.vertices[pointIndex] )
				#print(verts)
				pyglet.graphics.draw( 
					int(len(verts)/2), 
					pyglet.gl.GL_LINE_LOOP,
					('v2f', verts)
				)
				pass

		def drawRidgePoints(self):
			pyglet.gl.glColor4f(0,1,0,1)
			for ridgePoint in self.ridgePoints:
				verts = []
				#print(region)
				for pointIndex in ridgePoint:
					#print("Vertices length: " + str(len(self.vertices)))
					#print(pointIndex)
					verts.extend( self.vertices[pointIndex] )
				#print(verts)
				pyglet.graphics.draw( 
					int(len(verts)/2), 
					pyglet.gl.GL_POINTS,
					('v2f', verts)
				)
				pyglet.graphics.draw( 
					int(len(verts)/2), 
					pyglet.gl.GL_LINES,
					('v2f', verts)
				)
				pass

		def drawRidgeVertices(self):
			pyglet.gl.glColor4f(0,0,1,1)
			for ridgeVertex in self.ridgeVertices:
				verts = []
				#print(region)
				leavingEdge = False
				for pointIndex in ridgeVertex:
					if pointIndex == -1:
						leavingEdge = True
						print("Found a leaving edge")
						break
				if leavingEdge:		
					for pointIndex in ridgeVertex:
						#print("Vertices length: " + str(len(self.vertices)))
						#print(pointIndex)
						verts.extend( self.vertices[pointIndex] )
				#print(verts)
				pyglet.graphics.draw( 
					int(len(verts)/2), 
					pyglet.gl.GL_POINTS,
					('v2f', verts)
				)
				pyglet.graphics.draw( 
					int(len(verts)/2), 
					pyglet.gl.GL_LINES,
					('v2f', verts)
				)
				pass

		def drawFilledCells(self):
			#print("Drawing filled cells:")
			for cell in self.cellObjs.values():
				#print("Cell:")
				#print(cell.centre)
				#print(cell.points)
				cell.drawFilledCell()
				#break

		def drawCellObjBorders(self):
			for cell in self.cellObjs.values():
				cell.drawCellBorder()

		def addPointsForDrawing(self, newPoints=[]):			
			if newPoints:
				self.points.extend(newPoints)
				print("Adding " + str(len(newPoints)) + " points to those drawn. Total: " + str(len(self.points)))
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

		def drawAreaLimit(self):
			#print("Draw area limit")
			verts = []
			verts.extend([self.xInterval[0],self.yInterval[0]])
			verts.extend([self.xInterval[1],self.yInterval[0]])
			verts.extend([self.xInterval[1],self.yInterval[1]])
			verts.extend([self.xInterval[0],self.yInterval[1]])
			#print("Drawing point space with verts:")
			#print(verts)
			pyglet.gl.glColor4f(1,1,1,1)
			pyglet.graphics.draw( 
				int(len(verts)/2), 
				pyglet.gl.GL_LINE_LOOP,
				('v2f', verts)
			)

		def findHoveredCell(self):
			#print("Finding hovered cell for mouse: " + str(self.mouseX) + ", " + str(self.mouseY))
			cell = self.findContainingCell(self.mouseX, self.mouseY)
			if cell and self.hoveredCell != cell:
				self.hoveredCell = cell
				return True
			return False

		def findContainingCell(self, x, y):
			chosenCell = None
			minDistance = 99999999
			for cell in self.cellObjs.values():
				distSqd = math.sqrt((cell.vorCentre.coords[0] - x)**2 + (cell.vorCentre.coords[1] - y)**2)
				if distSqd < minDistance:
					chosenCell = cell
					#print("New chosen key is for cell " + str(self.cellObjs[chosenKey]))
					minDistance = distSqd
			#print("Min distance was: " + str(minDistance))
			#print("Id for that cell is: ")
			if chosenCell:
				#print("Chosen cell avg points:")
				#x = [n.coords[0] for n in chosenCell.points]
				#y = [n.coords[1] for n in chosenCell.points]
				#print(sum(x)/len(x))
				#print(sum(y)/len(y))
				return chosenCell
			return None

		def drawCellObjTrueCentres(self):			
			for cell in self.cellObjs.values():
				col = cell.color
				cell.trueCentre.drawPoint((col[0], col[1], col[2], 1))

		def drawHoverCellTrueCentre(self):
			if self.hoveredCell:
				self.hoveredCell.trueCentre.drawPoint((1,1,1,1))

		def drawHoverCellVoronoiCentre(self):
			if self.hoveredCell:
				self.hoveredCell.vorCentre.drawPoint((1,1,1,1))

		def highlightHoveredCell(self):
			if self.hoveredCell:
				col = self.hoveredCell.color
				self.hoveredCell.drawFilledCell((col[0], col[1], col[2], 0.6))