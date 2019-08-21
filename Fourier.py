from graphics import *
from math import *
from time import *
from random import *

class Phasor():
	def __init__(self, frequency, magnitude, phase=0):
		self.frequency = frequency
		self.magnitude = magnitude
		self.phase = phase
	
	def __str__(self):
		return "Frequency: " + str(self.frequency) + "  Magnitude: " + str(self.magnitude)
	def __repr__(self):
		return str(self)
	def __lt__(self, other):
		return abs(self.frequency) < abs(other.frequency)
	
	def generateCircle(self, start_x, start_y):
		return Circle(Point(start_x, start_y), self.magnitude)
	
	def generateArrow(self, start_x, start_y, timeStamp):
		angle = 2*pi*timeStamp*self.frequency + self.phase
		new_x = start_x + self.magnitude * cos(angle)
		new_y = start_y + self.magnitude * sin(angle)
		return Line(Point(start_x, start_y), Point(new_x, new_y)), new_x, new_y
	
	def is_Phasor():
		return True
		
class Fourier():
	def __init__(self):
		self.content={}
		
	def addPhasor(self, frequency, magnitude, phase=0):
		if int(frequency) != frequency:
			print("Frequency not accepted: " + str(frequency))
		else:
			self.content[frequency]=Phasor(frequency, magnitude, phase)
	
	def generateShapes(self, timeStamp):
		start_x = 0
		start_y = 0
		shapeList = []
		for p in sorted(foo.content.values()):
			c = p.generateCircle(start_x,start_y)
			l, next_x, next_y = p.generateArrow(start_x,start_y,timeStamp)
			l.setArrow("last")
			shapeList.append(c)
			shapeList.append(l)
			start_x, start_y = next_x, next_y
		return shapeList, start_x, start_y
		
	def display(self, frameTotal=100, displayArrows=True, DisplayTime=0):
		track_x = 0
		track_y = 0
		frameDuration = DisplayTime/frameTotal
		for frame in range(frameTotal+1):
			timeStamp = frame/frameTotal
			shape_list, new_x, new_y = self.generateShapes(timeStamp)
			if frame > 0:
				pencil_line = Line(Point(track_x, track_y), Point(new_x, new_y))
				pencil_line.draw(win)
			track_x, track_y = new_x, new_y
			if displayArrows:
				for shape in shape_list:
					shape.draw(win)
				sleep(frameDuration)
				for shape in shape_list:
					shape.undraw()
			
def TriangleByParam(p=0):
	x=0
	y=0
	if p<0:
		return Point(0,0)
	elif p<1:
		x = (sqrt(3)/4) * (2 - 3*p)
		y = (3/4)*p
		return Point(x,y)
	elif p<2:
		x = -(sqrt(3)/4)
		y = (9/4) - (6/4)*p
		return Point(x,y)
	elif p<=3:
		x = (sqrt(3)/4) * (-7 + 3*p)
		y = -(9/4) + (3/4)*p
		return Point(x,y)
	return Point(0,0)

def getTriangle(length, frameCount):
	pointList = []
	for frame in range(frameCount+1):
		timeStamp = length * frame/frameCount
		pointList.append(TriangleByParam(timeStamp))
	return pointList

def SquareByParam(p=0):
	x=0
	y=0
	if p<0:
		return Point(0,0)
	elif p<1:
		x = 1
		y = -1 + p*2
		return Point(x,y)
	elif p<2:
		x = 1-(p-1)*2
		y = 1
		return Point(x,y)
	elif p<3:
		x = -1
		y = 1-(p-2)*2
		return Point(x,y)
	elif p<=4:
		x = -1+(p-3)*2
		y = -1
		return Point(x,y)
	return Point(0,0)

def getSquare(length, frameCount):
	pointList = []
	for frame in range(frameCount+1):
		timeStamp = length * frame/frameCount
		pointList.append(SquareByParam(timeStamp))
	return pointList

def displayPoints(list, window):
	track_x = 0
	track_y = 0
	for i in range(len(list)):
		if i > 0:
			pencil_line = Line(list[i-1], list[i])
			pencil_line.draw(window)
	return

def rotatePoint(pt, angleShift):
	x = pt.getX()*cos(angleShift) - pt.getY()*sin(angleShift)
	y = pt.getY()*cos(angleShift) + pt.getX()*sin(angleShift)
	return Point(x, y)

def rotatePaper(shp, freq):
	newShp=[]
	for i in range(len(shp)):
		theta = (-freq * 2 * pi)*(i/len(shp))
		newPoint = rotatePoint(shp[i], theta)
		newShp.append(newPoint)
	return newShp

def getCentre(shp, freq):
	x_total=0
	y_total=0
	scale = len(shp)-1
	for i in range(1, scale+1):
		theta = (-freq * 2 * pi)*(i/len(shp))
		newPoint = rotatePoint(shp[i], theta)
		x_total += newPoint.getX()
		y_total += newPoint.getY()
	x = x_total / scale
	y = y_total / scale
	magnitude = sqrt(x**2 + y**2)
	phase = atan(y/x)
	return (freq, magnitude, phase)
		
win = GraphWin("My Circle", 1000, 1000)
coordScale = 2.5
win.setCoords(-coordScale,-coordScale,coordScale,coordScale)
frameTotal=4000

triangle = getTriangle(3,frameTotal)
square   = getSquare(4,frameTotal)
foo = Fourier()

for i in range(-30, 30):
	newPh = getCentre(square, i)
	foo.addPhasor(newPh[0], newPh[1], newPh[2])


#for freq in range(1, 30):
#	foo.addPhasor(freq, random()*5/freq, 2*pi*random())
#foo.addPhasor(1, 2 + random()*3, 2*pi*random())
#displayPoints(square,win)
#win.getMouse()
foo.display(400, False)
win.getMouse()

