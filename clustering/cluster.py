#import _version
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import warnings
from numbers import Integral


class KMeansPlusPlus:

    def __init__(self, data_frame, k, columns=None, max_iterations=None, appended_column_name=None):
        if not isinstance(data_frame, DataFrame):
            raise Exception("data_frame argument is not a pandas DataFrame")
        elif data_frame.empty:
            raise Exception("The given data frame is empty")

        if max_iterations is not None and max_iterations <= 0:
            raise Exception("max_iterations must be positive!")

        if not isinstance(k, Integral) or k <= 0:
            raise Exception("The value of k must be a positive integer")

        self.data_frame = data_frame  # m x n
        self.numRows = data_frame.shape[0]  # m

        # k x n, the i,j entry being the jth coordinate of center i
        self.centers = None

        # m x k , the i,j entry represents the distance
        # from point i to center j
        # (where i and j start at 0)
        self.distance_matrix = None

        # Series of length m, consisting of integers 0,1,...,k-1
        self.clusters = None

        # To keep track of clusters in the previous iteration
        self.previous_clusters = None

        self.max_iterations = max_iterations
        self.appended_column_name = appended_column_name
        self.k = k

        if columns is None:
            self.columns = data_frame.columns
        else:
            for col in columns:
                if col not in data_frame.columns:
                    raise Exception(
                        "Column '%s' not found in the given DataFrame" % col)
                if not self._is_numeric(col):
                    raise Exception(
                        "The column '%s' is either not numeric or contains NaN values" % col)
            self.columns = columns

    def _populate_initial_centers(self):
        rows = []
        rows.append(self._grab_random_point())
        distances = None

        while len(rows) < self.k:
            if distances is None:
                distances = self._distances_from_point(rows[0])
            else:
                distances = self._distances_from_point_list(rows)

            normalized_distances = distances / distances.sum()
            normalized_distances.sort()
            dice_roll = np.random.rand()
            min_over_roll = normalized_distances[
                normalized_distances.cumsum() >= dice_roll].min()
            index = normalized_distances[
                normalized_distances == min_over_roll].index[0]
            rows.append(self.data_frame[self.columns].iloc[index, :])

        self.centers = DataFrame(rows, columns=self.columns)

    def _compute_distances(self):
        if self.centers is None:
            raise Exception(
                "Must populate centers before distances can be calculated!")

        column_dict = {}

        for i in list(range(self.k)):
            column_dict[i] = self._distances_from_point(
                self.centers.iloc[i, :])

        self.distance_matrix = DataFrame(
            column_dict, columns=list(range(self.k)))

    def _get_clusters(self):
        if self.distance_matrix is None:
            raise Exception(
                "Must compute distances before closest centers can be calculated")

        min_distances = self.distance_matrix.min(axis=1)

        # We need to make sure the index
        min_distances.index = list(range(self.numRows))

        cluster_list = [boolean_series.index[j]
                        for boolean_series in
                        [
                            self.distance_matrix.iloc[i,
                                                      :] == min_distances.iloc[i]
                            for i in list(range(self.numRows))
                        ]
                        for j in list(range(self.k))
                        if boolean_series[j]
                        ]

        self.clusters = Series(cluster_list, index=self.data_frame.index)

    def _compute_new_centers(self):
        if self.centers is None:
            raise Exception("Centers not initialized!")

        if self.clusters is None:
            raise Exception("Clusters not computed!")

        for i in list(range(self.k)):
            self.centers.ix[i, :] = self.data_frame[
                self.columns].ix[self.clusters == i].mean()

    def cluster(self):

        self._populate_initial_centers()
        self._compute_distances()
        self._get_clusters()

        counter = 0

        while True:
            counter += 1

            self.previous_clusters = self.clusters.copy()

            self._compute_new_centers()
            self._compute_distances()
            self._get_clusters()

            if self.max_iterations is not None and counter >= self.max_iterations:
                break
            elif all(self.clusters == self.previous_clusters):
                break

        if self.appended_column_name is not None:
            try:
                self.data_frame[self.appended_column_name] = self.clusters
            except:
                warnings.warn(
                    "Unable to append a column named %s to your data." %
                    self.appended_column_name)
                warnings.warn(
                    "However, the clusters are available via the cluster attribute")

    def _distances_from_point(self, point):
        # pandas Series
        return np.power(self.data_frame[self.columns] - point, 2).sum(axis=1)

    def _distances_from_point_list(self, point_list):
        result = None

        for point in point_list:
            if result is None:
                result = self._distances_from_point(point)
            else:
                result = pd.concat(
                    [result, self._distances_from_point(point)], axis=1).min(axis=1)

        return result

    def _grab_random_point(self):
        index = np.random.random_integers(0, self.numRows - 1)
        # NumPy array
        return self.data_frame[self.columns].iloc[index, :].values

    def _is_numeric(self, col):
        return all(np.isreal(self.data_frame[col])) and not any(np.isnan(self.data_frame[col]))
