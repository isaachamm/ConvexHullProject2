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
		lines = [line]
		self.view.addLines(lines,color)
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
		# Done by implementing the quicksort and partition algorithm

		def partition(start_index, end_index):
			# Choose a pivot at random –– constant time
			# Necessary because it makes quicksort more likely to run average time nlogn, instead of
			# 	worst case time, n^2
			pivot_index = random.randint(start_index, end_index)

			# Move the pivot point out of the way (to the start of the array) -- constant time
			points[pivot_index], points[start_index] = points[start_index], points[pivot_index]

			# index of smaller element
			low = start_index

			# high is a looper variable that keeps track of the current index
			# This is where the O(n) work comes in –- comparisons of numbers and merging of two halves
			for high in range(start_index + 1, end_index + 1):
				# if math.isclose(points[high].x() < points[pivot_index].x()) :
				#Don't need the above because we're not performing arithmetic, just comparisons on bounded numbers
				if points[high].x() < points[start_index].x():
					low += 1
					points[low], points[high] = points[high], points[low]

			# Move the pivot back to the new correct position
			points[low], points[start_index] = points[start_index], points[low]

			return low

		def quicksort(start_index, end_index) :

			# overall, quicksort is O(n log n) time
			# Quicksort does the logn work as it splits the array in half until it reaches 1 element
			# the partition function does the n work as it does the comparisons and recombines
			if start_index < end_index:
				partition_index = partition(start_index, end_index)
				quicksort(start_index, partition_index - 1)
				quicksort(partition_index + 1, end_index)

		quicksort(0, len(points) - 1)
		# points.sort(key = lambda p: p.x())

		t2 = time.time()

		t3 = time.time()

		def convex_hull_solver(point_array) :
			if len(point_array) == 0:
				return
			elif len(point_array) == 1:
				# base case = only 1 point left
				return point_array[0]
			else:
				# This is where the divide occurs – logn time
				left_points = convex_hull_solver(point_array[:(len(point_array) // 2)])	# left-side recurse
				right_points = convex_hull_solver(point_array[(len(point_array) // 2):]) # right-side recurse

				print(left_points)
				print(right_points)

				def find_upper_tangent(left_side, right_side):
					rm_left_point = None
					lm_right_point = None
					if type(left_points) is not list:
						rm_left_point = left_points
					else:
						rm_left_point = left_side[:-1]

					if type(right_points) is not list:
						lm_right_point = right_points
					else:
						lm_right_point = right_side[0]

					slope = (rm_left_point.y() - lm_right_point.y()) / (rm_left_point.x() - lm_right_point.x())


					# for left_point in left_side:
					# 	if ()

					return

				find_upper_tangent(left_points, right_points)

				def find_lower_tangent():
					return
		# 	while either of the tangent functions change the tangent lines
		# 		call upper tangent function
		# 		call lower tangent function
		# 	return combined hulls, or it won't recurse back up

		convex_hull_solver(points)


		# this is a dummy polygon of the first 3 unsorted points
		polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER


		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
