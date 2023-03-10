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
		# SORT THE POINTS BY INCREASING X-VALUE
		# Done by implementing the quicksort and partition algorithm

		def partition(start_index, end_index):
			# Choose a pivot at random –– constant time
			# Necessary to choose randomly because it makes quicksort more likely to run average time nlogn, instead of
			# 	worst case time, n^2
			pivot_index = random.randint(start_index, end_index)

			# Move the pivot point out of the way (to the start of the array) -- constant time
			points[pivot_index], points[start_index] = points[start_index], points[pivot_index]

			# index of smaller element
			low = start_index

			# high is a looper variable that keeps track of the current index
			# This is where the O(n) work comes in –- comparisons of numbers and merging of two halves
			# 	We do this O(log n) times, thus O(n log n)
			for high in range(start_index + 1, end_index + 1):
				# if math.isclose(points[high].x() < points[pivot_index].x()) :
				# Don't need the above because we're not performing arithmetic, just comparisons on bounded numbers
				if points[high].x() < points[start_index].x():
					low += 1
					points[low], points[high] = points[high], points[low]

			# Move the pivot back to the new correct position – constant time
			points[low], points[start_index] = points[start_index], points[low]

			return low

		def quicksort(start_index, end_index) :

			# overall, quicksort is O(n log n) time
			# Quicksort does the log n work as it splits the array in half until it reaches 1 element
			# The partition function does the n work as it does the comparisons and recombines
			if start_index < end_index:
				partition_index = partition(start_index, end_index)
				quicksort(start_index, partition_index - 1)
				quicksort(partition_index + 1, end_index)

		quicksort(0, len(points) - 1)
		# This is a built in Python function that accomplishes the same thing:
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
				# This is where the divide occurs – log n time, because we're dividing in half every time
				# At this point, everything will be sorted in clockwise order. To change to counter-clockwise,
				# 	You'd have to reverse the right list.
				left_points = convex_hull_solver(point_array[:(len(point_array) // 2)])	# left-side recurse
				right_points = convex_hull_solver(point_array[(len(point_array) // 2):]) # right-side recurse

				# print(left_points)
				# print(right_points)

				def find_lower_tangent(left_side, right_side):
					left_side_point = None  # start with right-most point on the left hull
					right_side_point = None # start with left-most point on the right hull

					# Check for base case (a single point)
					if type(left_side) is not list:
						left_side_point = left_side
					else:
						# Find the minimum x-value (need to do this for when we order clockwise)
						# Comparison is O(1) constant time, but worst case would be going through all x-values in each
						# 	sub-hull, so O(n) time
						left_side_point = left_side[0]
						for point in left_side:
							if left_side_point.x() < point.x():
								left_side_point = point	

					if type(right_side) is not list:
						right_side_point = right_side
					else:
						right_side_point = right_side[0]
						for point in right_side:
							if right_side_point.x() > point.x():
								right_side_point = point

					# Calculate and compare slopes
					change_occurred = True
					while change_occurred:

						# Showing tangent lines for debugging
						# tangent_line = QLineF(left_side_point, right_side_point)
						# self.showTangent(tangent_line, GREEN)

						change_occurred = False

						# Each of these performs at least one multiplication or division, so O(n^2) for bitwise
						# 	arithmetic complexity
						slope = (left_side_point.y() - right_side_point.y()) / (left_side_point.x() - right_side_point.x())

						# check for base case
						if type(left_side) is list:
							for i in range(len(left_side)):
								new_slope = (left_side[i].y() - right_side_point.y()) / (left_side[i].x() - right_side_point.x())
								if new_slope > slope:
									left_side_point = left_side[i]
									change_occurred = True
									break

						# Save time not calculating for both until the left side is already done
						if change_occurred: continue

						if type(right_side) is list:
							for i in range(len(right_side)):
								new_slope = (right_side[i].y() - left_side_point.y()) / (right_side[i].x() - left_side_point.x())
								if new_slope < slope:
									right_side_point = right_side[i]
									change_occurred = True
									break

					return [left_side_point, right_side_point]

				def find_upper_tangent(left_side, right_side):
					left_side_point = None  # start with right-most point on the left hull
					right_side_point = None # start with left-most point on the right hull
					if type(left_side) is not list:
						left_side_point = left_side
					else:
						left_side_point = left_side[0]
						for point in left_side:
							if left_side_point.x() < point.x():
								left_side_point = point

					if type(right_side) is not list:
						right_side_point = right_side
					else:
						right_side_point = right_side[0]
						for point in right_side:
							if right_side_point.x() > point.x():
								right_side_point = point


					change_occurred = True
					while change_occurred:

						''' This is for debugging '''
						# tangent_line = QLineF(left_side_point, right_side_point)
						# self.showTangent(tangent_line, GREEN)

						change_occurred = False

						# Calculate and compare slopes
						slope = (left_side_point.y() - right_side_point.y()) / (left_side_point.x() - right_side_point.x())

						if type(left_side) is list:
							for i in range(len(left_side)):
								new_slope = (left_side[i].y() - right_side_point.y()) / (left_side[i].x() - right_side_point.x())
								if new_slope < slope:
									left_side_point = left_side[i]
									change_occurred = True
									break

						# Save time not calculating for both until the left side is already done
						if change_occurred: continue

						if type(right_side) is list:
							for i in range(len(right_side)):
								new_slope = (right_side[i].y() - left_side_point.y()) / (right_side[i].x() - left_side_point.x())
								if new_slope > slope:
									right_side_point = right_side[i]
									change_occurred = True
									break


					return [left_side_point, right_side_point]
				# This will return a line that we will use to make the new hull
				upper_tangent = find_upper_tangent(left_points, right_points)
				lower_tangent = find_lower_tangent(left_points, right_points)

				# Base case check
				if type(left_points) is not list:
					new_hull = [left_points]
				else:
					# Start at the right upper tangent and loop counterclockwise around, adding points until we
					# 	get to the lower tangent
					new_hull = [upper_tangent[1]]
					left_side_counter = left_points.index(upper_tangent[0])
					new_hull.append(left_points[left_side_counter])

					# while – you don't hit the "end point" –– the lower tangent, at which point we switch to the other
					# 	side's lower tangent
					# Time complexity of this: O(<n) because while we are looping through points, we are only adding
					# 	those that are on the hull, a number far less than n. Worst case would be O(n)
					while True:
						# We break with this if because we connect to the other sub-hull at this point
						if left_points[left_side_counter] == lower_tangent[0]:
							break
						left_side_counter += 1
						left_side_counter = left_side_counter % len(left_points)
						new_hull.append(left_points[left_side_counter])

				# Same thing as above for right side
				if type(right_points) is not list:
					new_hull.append(right_points)
				else:
					right_side_counter = right_points.index(lower_tangent[1])
					new_hull.append(right_points[right_side_counter])

					while True:
						right_side_counter += 1
						right_side_counter = right_side_counter % len(right_points)
						new_hull.append(right_points[right_side_counter])
						if right_points[right_side_counter] == upper_tangent[1]:
							break

				''' this is for debugging '''
				# new_hull_size = len(new_hull)
				# recursion_polygon = [QLineF(new_hull[i], new_hull[(i + 1) % new_hull_size]) for i in range(len(new_hull))]
				# self.showHull(recursion_polygon, BLUE)
				# self.eraseHull(recursion_polygon)

				# This return is the ordered set of points that make up the new hull
				return new_hull


		hull = convex_hull_solver(points)
		hull_size = len(hull) - 1
		# This for loop is O(<n) because it only contains points on the hull
		polygon = [QLineF(hull[i], hull[(i + 1) % hull_size]) for i in range(len(hull))]

		t4 = time.time()

		# print(t2 - t1)
		# print(t4 - t3)

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
