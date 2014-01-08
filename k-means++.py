from pandas import DataFrame,Series
import pandas as pd
import numpy as np
from numbers import Integral

class KMeansPlusPlus:
	def __init__(self,dataFrame,k,columns=None,maxIterations=None):
		if not isinstance(dataFrame,DataFrame):
			raise Exception("dataFrame argument is not a pandas DataFrame")
		elif dataFrame.empty:
			raise Exception("The given data frame is empty")

		self.dataFrame = dataFrame
		self.numRows = dataFrame.shape[0]
		self.centers = None
		self.distance_matrix = None

		if not isinstance(k,Integral) or k <= 0:
			raise Exception("The value of k must be a positive integer")

		self.k = k

		if columns is None:
			self.columns = dataFrame.columns
		else:
			for col in columns:
				if col not in dataFrame.columns:
					raise Exception("Column '%s' not found in the given DataFrame" % col)
				if not self.__is_numeric(col):
					raise Exception("The column '%s' is either not numeric or contains NaN values" % col)
			self.columns = columns

	def __populate_initial_centers(self):
		rows = []
		rows.append(self.__grab_random_point())
		distances = None

		while len(rows) < self.k:
			if distances is None:
				distances = self.__distances_from_point(rows[0])
			else:
				distances = self.__distances_from_point_list(rows)

			normalized_distances = distances/distances.sum()
			normalized_distances.sort()
			dice_roll = np.random.rand()
			min_over_roll = normalized_distances[normalized_distances.cumsum() >= dice_roll].min()
			index = normalized_distances[normalized_distances == min_over_roll].index[0]
			rows.append(self.dataFrame[self.columns].irow(index))

		self.centers = DataFrame(rows)

	def __compute_distances(self):
		if self.centers is None:
			raise Exception("Must populate centers before distances can be calculated!")

		column_dict = {}

		for i in list(range(self.k)):
			column_dict[i] = self.__distances_from_point(self.centers.irow(i))

		self.distance_matrix = DataFrame(column_dict,columns=list(range(self.k)))







	def __distances_from_point(self,point):
		return np.power(self.dataFrame[columns] - point,2).sum(axis=1) #pandas Series

	def __distances_from_point_list(self,point_list):
		result = None

		for point in point_list:
			if result is None:
				result = self.__distances_from_point(point)
			else:
				result = pd.concat([result,self.__distances_from_point(point)],axis=1).min(axis=1)

		return result




	def __grab_random_point(self):
		index = np.random.random_integers(0,self.numRows - 1)
		return self.dataFrame[self.columns].irow(index).values #NumPy array




	def __is_numeric(self,col):
		return all(np.isreal(self.dataFrame[col])) and not any(np.isnan(self.dataFrame[col]))