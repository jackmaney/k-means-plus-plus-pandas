from pandas import DataFrame,Series
import pandas as pd
import numpy as np

class KMeansPlusPlus:
	def __init__(self,dataFrame,columns=None,maxIterations=None):
		if not isinstance(dataFrame,DataFrame):
			raise Exception("dataFrame argument is not a pandas DataFrame")
		elif dataFrame.empty:
			raise Exception("The given data frame is empty")

		self.dataFrame = dataFrame
		self.numRows = dataFrame.shape[0]

		if columns is None:
			self.columns = dataFrame.columns
		else:
			for col in columns:
				if col not in dataFrame.columns:
					raise Exception("Column '%s' not found in the given DataFrame" % col)
				if not self.__is_numeric(col):
					raise Exception("The column '%s' is either not numeric or contains NaN values" % col)
			self.columns = columns

	def distance_from_point(self,point):
		if not isinstance(point,np.array):
			raise Exception("Argument '%s' is not a NumPy ndarray" % point)
		elif point.ndim != 1:
			raise Exception("One-dimensional points only, please.")
		elif point.shape[0] != len(self.columns):
			raise Exception("The point '%s' is not of the same dimension as the given set of columns" % point)

		return np.power(self.dataFrame[columns] - point,2).sum(axis=1) #pandas Series


	def __is_numeric(self,col):
		return all(np.isreal(self.dataFrame[col])) and not any(np.isnan(self.dataFrame[col]))