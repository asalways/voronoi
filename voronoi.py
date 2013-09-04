import math
import random
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet import image

#Mouse interaction
from pyglet.window import mouse

import numpy
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

import draw
import geometry

# Takes a list of points as input, or generates its own if none

class VoronoiDiagram():
	def __init__(self, points=[], totalPoints=700, width=800, height=800):
		self.points = points
		self.width = width
		self.height = height 
		if not self.points:
			#self.points = self.generatePoints(totalPoints)
			#self.points = self.generateJitteredGridPoints()
			#self.points = self.generateGridPoints()
			self.points = self.generatePoissonDiskPoints()
		else:
			totalPoints = len(self.points)
		# Add sample points for corners of region
		#self.addBoundaryPoints(width, height)

	def applyMarginToPoints(self, xMargin, yMargin):
		for i in range(len(self.points)):
			self.points[i] = [ self.points[i][0]+xMargin, self.points[i][1]+yMargin ]

	def generatePoints(self, totalPoints):
		newPoints = [ (random.random()*self.width, random.random()*self.height) for x in range(totalPoints) ]
		return newPoints

	def generateGridPoints(self, gridDivs=10):
		cellWidth = self.width / gridDivs
		cellHeight = self.height / gridDivs
		xStart = cellWidth / 2
		yStart = cellHeight / 2
		newPoints = []
		for xStep in range(gridDivs):
			x = xStart + (cellWidth * xStep)
			for yStep in range(gridDivs):
				y = yStart + (cellHeight * yStep)
				newPoints.extend([(x, y)])
		return newPoints

	def generateJitteredGridPoints(self, gridDivs=50):
		cellWidth = self.width / gridDivs
		cellHeight = self.height / gridDivs

		gridPoints = self.generateGridPoints(gridDivs)
		points = []
		for n in range(len(gridPoints)):
			# x and y are centre of each grid cell
			xJitter = 0
			yJitter = 0
			# Debug if statement for turning off jitter to obtain uniform grid
			useJitter = True
			if useJitter:
				xJitter = (random.random() * cellWidth) - (cellWidth / 2)
				yJitter = (random.random() * cellHeight) - (cellHeight / 2)
			points.extend( [ (gridPoints[n][0] + xJitter, gridPoints[n][1] + yJitter) ] )
		return points

	def generatePoissonDiskPoints(self, minDist=75):
		# Cell contains single point only; dim is a function of min dist between points
		cellDim = math.sqrt(minDist)

		xBuffer = int(self.width * 0.2)
		xMax = self.width + 2*xBuffer
		yBuffer = int(self.height * 0.2)
		yMax = self.height + 2*yBuffer

		firstPoint = (random.random()*xMax, random.random()*yMax)
		processList = [firstPoint]
		# 2D array is a list of lists
		xCells = int(xMax / cellDim) + 1
		yCells = int(yMax / cellDim) + 1
		grid = [[()*yCells]*(xCells) for n in range(xCells)]
		##print("MaxGrid: " + str(xCells) + ", " + str(yCells))
		# Add first point to 2d array
		grid[int(firstPoint[0]/cellDim)][int(firstPoint[1]/cellDim)] = firstPoint
		# k is number of points attempted to be placed
		k = 30
		# Process points until all have been processed
		outputPoints = []
		while processList:
			# Remove a random points from the process list
			nextCentrePoint = processList.pop(int(random.random()*len(processList)))
			for i in range(k):
				# Generate random points around nextPoint
				r1 = random.random()
				r2 = random.random()
				radius = minDist * (r1 + 1)
				# random angle
				angle = 2 * math.pi * r2
				newX = nextCentrePoint[0] + radius * math.cos(angle)
				newY = nextCentrePoint[1] + radius * math.sin(angle)
				if newX < 0 or newX > xMax or newY < 0 or newY > yMax:
					# Only accept points within the bounds of the screen space
					continue
				newPoint = (newX, newY)				
				#print("newPoint: " + str(newPoint))

				# Check neighbourhood for points too close
				tooClose = False
				gridX = int(newPoint[0]/cellDim)
				gridY = int(newPoint[1]/cellDim)
				##print("newPoint gridLocs: " + str(gridX) + ", " + str(gridY))
				# Get neighbourhood around point
				for xOffset in range(-2,3):
					nX = gridX + xOffset
					if nX < 0 or nX > int(xMax/cellDim):
						# Skip out-of-bounds cells
						##print("Skipping gridX of " + str(nX))
						continue
					for yOffset in range(-2,3):
						nY = gridY + yOffset
						if nY < 0 or nY > int(yMax/cellDim):
							# Skip out-of-bounds cells
							##print("Skipping gridY of " + str(nY))
							continue
						##print("nX: " + str(nX) + ", nY: " + str(nY))
						if grid[nX][nY]:						
							# Grid cell contains a point
							nPoint = grid[nX][nY]
							#print(grid)
							#print("nPoint: " + str(nPoint))
							#print("newPoint: " + str(newPoint))
							xDiff =  nPoint[0]-newPoint[0]
							yDiff = nPoint[1]-newPoint[1]
							dist = math.hypot( nPoint[0]-newPoint[0], nPoint[1]-newPoint[1] )
							if dist < minDist:
								tooClose = True

				# Accept valid points
				if not tooClose:
					processList.extend([newPoint])
					outputPoints.extend([newPoint])
					##print("Grid len: " + str(len(grid)))
					##print("Adding point with grid locs: " + str(gridX) + ", " + str(gridY))
					grid[gridX][gridY] = newPoint

		# Shift all points the buffer distance to re-centre diagram
		finalPoints = []
		for point in outputPoints:
			finalPoints.append( (point[0] - xBuffer, point[1] - yBuffer) )
		# Return poisson disks points output
		return finalPoints

	def addBoundaryPoints(self, xDim, yDim):
		boundaryPoints = [(0,0), (0,yDim), (xDim, 0), (xDim, yDim)]
		self.points.extend(boundaryPoints)

xDim = 800
yDim = 600

# Mask image
#maskImage = pyglet.resource.image('groundtruth5.bmp')


v = VoronoiDiagram( totalPoints=700, width=xDim, height=yDim)
xMargin = 10
yMargin = 10
# Shifts all points according to size of margin
v.applyMarginToPoints(xMargin, yMargin)

#print("jitter")
#cellWidth = 10
#cellHeight = 10
#for i in range(30):
#	xJitter = (random.random() * cellWidth) - (cellWidth / 2)
#	yJitter = (random.random() * cellHeight) - (cellHeight / 2)
#	print(str(xJitter) + " " + str(yJitter))

w = draw.DiagramWindow(v.width+2*xMargin, v.height+2*yMargin, [xMargin, xMargin+xDim], [yMargin, yMargin+yDim])

# Scipy Voronoi #
vor = Voronoi(v.points)
#voronoi_plot_2d(vor)
#plt.show()

w.vertices.extend(vor.vertices)
#print(w.vertices)
w.ridgePoints.extend(vor.ridge_points)
#print(w.ridgePoints)
w.ridgeVertices.extend(vor.ridge_vertices)
#print(w.ridgeVertices)
w.regions.extend(vor.regions)
#print(vor.regions)
##

def createPointObjs(vor):
	final = []
	for vertex in vor.vertices:
		final.append(geometry.Point(vertex[0], vertex[1]))
	return final

w.pointObjs = createPointObjs(vor)

def createCellObjs(initialPoints, vor, pointObjs):
	final = dict()
	#print("Total regions:")
	#print(len(vor.regions))
	#print("Total points:")
	#print(len(vor.points))
	for i in range(len(vor.points)):
		#print("i: " + str(i))
		# There are half as many points as there are values in initialPoints (is 2d)
		#print(vor.points)
		#print(vor.points[i*2])
		newCentre = geometry.Point(vor.points[i][0], vor.points[i][1])
		#print(newCentre.coords)
		# Use index i to find set of points surrounding region
		points = []
		for n in vor.regions[i]:
			#print("n: " + str(n))
			# Use point objects rather than vertex information
			if n == -1:
				#print("N is minus 1")
				pass
			else:
				points.append(pointObjs[n])
		newCell = geometry.Cell( newCentre, points )
		final[newCell.trueCentre] = newCell
	return final

cellObjs = createCellObjs(v.points, vor, w.pointObjs)
#print(w.cellObjs)

def clampCellObjsToBoundary(cells, xInterval, yInterval):
	print("Total cells before discarding OOBs: " + str(len(cells)))
	clampedCells = dict()
	while cells:
		key = random.choice(cells.keys())
		cell = cells.pop(key)
		rejectCell = False	
		# Clamp all points to interval
		pointsClamped = 0
		xSum = 0
		ySum = 0
		for point in cell.points:
			wasClamped = False
			# Clamp x dimension
			if point.coords[0] <= xInterval[0]:
				point.coords[0] = xInterval[0]
				wasClamped = True
			elif point.coords[0] >= xInterval[1]:
				point.coords[0] = xInterval[1]
				wasClamped = True
			# Clamp y dimension
			if point.coords[1] <= yInterval[0]:
				point.coords[1] = yInterval[0]
				wasClamped = True
			elif point.coords[1] >= yInterval[1]:
				point.coords[1] = yInterval[1]
				wasClamped = True
			# Increment clamping counter if any dimension was clamped for this point
			if wasClamped:
				pointsClamped += 1
			# Track total x and y so average can be found for cell centre
			xSum += point.coords[0]
			ySum += point.coords[1]
		# Retain cell only if not all points were clamped
		if not pointsClamped == len(cell.points) and len(cell.points) > 0:
			clampedCells[cell.trueCentre] = cell
			# Calculate true centre as average of points
			#print("Cell points length: " + str(len(cell.points)))
			cell.trueCentre = geometry.Point(xSum/len(cell.points), ySum/len(cell.points))
			#print(cell.trueCentre.coords)
	print("Total cells after discarding OOBs: " + str(len(clampedCells)))
	return clampedCells

# Clamp dimensions for cellObjs and discard those which are completely out of bounds
cellObjs = clampCellObjsToBoundary(cellObjs, [xMargin, xMargin+xDim], [yMargin, yMargin+yDim])
w.cellObjs = cellObjs

w.addPointsForDrawing(v.points)
#w.addGridWidthForDrawing(math.sqrt(80))

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

pyglet.app.run()
