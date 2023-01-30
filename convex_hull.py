import math
import random

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE

		def partition(start_index, end_index):
			# Choose a pivot at random –– constant time
			pivot_index = random.randint(start_index, end_index)

			# Move the pivot point out of the way (to the start of the array) -- constant time
			points[pivot_index], points[start_index] = points[start_index], points[pivot_index]

			# index of smaller element
			low = start_index

			# high is a looper variable that keeps track of the current index
			for high in range(start_index + 1, end_index + 1):
				# if math.isclose(points[high].x() < points[pivot_index].x()) :
				if points[high].x() < points[start_index].x():
					low += 1
					points[low], points[high] = points[high], points[low]

			points[low], points[start_index] = points[start_index], points[low]

			return low

		def quicksort(start_index, end_index) :

			if start_index < end_index:
				partition_index = partition(start_index, end_index)
				quicksort(start_index, partition_index - 1)
				quicksort(partition_index + 1, end_index)

		quicksort(0, len(points) - 1)
		# points.sort(key = lambda p: p.x())

		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
