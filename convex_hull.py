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
				# At this point, everything will be sorted in clockwise order. To change to counter-clockwise,
				# 	You'd have to reverse the right list.
				left_points = convex_hull_solver(point_array[:(len(point_array) // 2)])	# left-side recurse
				right_points = convex_hull_solver(point_array[(len(point_array) // 2):]) # right-side recurse

				print(left_points)
				print(right_points)

				def find_upper_tangent(left_side, right_side):
					left_side_point = None  # start with right-most point on the left hull
					right_side_point = None # start with left-most point on the right hull
					if type(left_side) is not list:
						left_side_point = left_side
					else:
						# TODO: Need alternate way to find x-value
						left_side_point = left_side[-1]

					if type(right_side) is not list:
						right_side_point = right_side
					else:
						# TODO: Need alternate way to find x-value
						right_side_point = right_side[0]

					# Compare points on the previous hull to the line.
					# Adjust line (the slope and b need to be inside the while loop)
					change_occurred = True
					while change_occurred:

						change_occurred = False
						# We need to calculate slope and b for y = mx + b
						slope = (left_side_point.y() - right_side_point.y()) / (left_side_point.x() - right_side_point.x())
						b = right_side_point.y() - (slope * right_side_point.x())


						# Need this check for when either side is only one point
						if type(left_side) is list:
							for i in range(len(left_side)):
								if left_side[i].y() > ((slope * left_side[i].x()) + b):
									left_side_point = left_side[i]
									change_occurred = True

						# Save time not calculating for both until the left side is already done
						if change_occurred: continue

						# Need this check for when either side is only one point
						if type(right_side) is list:
							for i in range(len(right_side)):
								temp_point = right_side[i]
								if temp_point.y() > ((slope * temp_point.x()) + b):
									right_side_point = right_side[i]
									change_occurred = True

					return [left_side_point, right_side_point]

				def find_lower_tangent(left_side, right_side):
					left_side_point = None  # start with right-most point on the left hull
					right_side_point = None # start with left-most point on the right hull
					if type(left_side) is not list:
						left_side_point = left_side
					else:
						# TODO: Need alternate way to find x-value
						left_side_point = left_side[-1]

					if type(right_side) is not list:
						right_side_point = right_side
					else:
						# TODO: Need alternate way to find x-value
						right_side_point = right_side[0]


					change_occurred = True
					while change_occurred:

						change_occurred = False
						# We need to calculate slope and b for y = mx + b
						slope = (left_side_point.y() - right_side_point.y()) / (left_side_point.x() - right_side_point.x())
						b = right_side_point.y() - (slope * right_side_point.x())

						# Compare points on the previous hull to the line.
						# Adjust line (the slope and b need to be inside the while loop)
						# Need to do order differences
						# Need this check for when either side is only one point
						if type(left_side) is list:
							for left_point in left_side:
								if left_point.y() < ((slope * left_point.x()) + b):
									left_side_point = left_point
									change_occurred = True

						# Save time not calculating for both until the left side is already done
						if change_occurred: continue

						# Need this check for when either side is only one point
						if type(right_side) is list:
							for right_point in right_side:
								if right_point.y() < ((slope * right_point.x()) + b):
									right_side_point = right_point
									change_occurred = True

					return [left_side_point, right_side_point]
				# This will return a line that we will use to make the new hull
				upper_tangent = find_upper_tangent(left_points, right_points)
				lower_tangent = find_lower_tangent(left_points, right_points)

				new_hull = None

				# This is the upper tangent point on the left side –- where we'll start keeping track
				add_points = False

				# We have to multiply by 2 here to make sure that we get all the points from the UT to the LT
				if left_points is not list:
					new_hull = [left_points]
				else:
					for i in range(len(left_points) * 2):
						index = i % len(left_points)

						if left_points[index] == upper_tangent[0]:
							new_hull = upper_tangent[0]
							add_points = True

						if add_points:
							new_hull.append(left_points[index])

						if left_points[index] == lower_tangent[0]:
							# Don't add here because we already added just above
							add_points = False
							break

				if right_points is not list:
					new_hull.append(right_points)
				else:
					for i in range(len(right_points) * 2):
						index = i % len(right_points)

						if right_points[index] == lower_tangent[1]:
							add_points = True

						if add_points:
							new_hull.append(right_points[index])

						if right_points[index] == upper_tangent[1]:
							add_points = False
							break

				return new_hull


		# 	while either of the tangent functions change the tangent lines
		# 		call upper tangent function
		# 		call lower tangent function
		# 	return combined hulls, or it won't recurse back up

		# this is a dummy polygon of the first 3 unsorted points
		polygon = convex_hull_solver(points)

		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
