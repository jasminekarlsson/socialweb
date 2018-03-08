import numpy as np
from scipy.sparse import dok_matrix

class Matrix:
    m = None
    user_indexes = {}
    last_index = -1

    def __init__(self, nrows, ncolumns):
        self.m = dok_matrix((nrows, ncolumns))

    def _addUser(self, u):
        self.last_index = self.last_index + 1
        self.user_indexes[u] = self.last_index

    def setWeight(self, u1, u2, weight):
        if u1 not in self.user_indexes:
            self._addUser(u1)
        if u2 not in self.user_indexes:
            self._addUser(u2)

        self.m[self.user_indexes[u1], self.user_indexes[u2]] = weight


    def getWeight(self, u1, u2):
        return self.m[self.user_indexes[u1], self.user_indexes[u2]]
