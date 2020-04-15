from collections import deque
import math


class FloydWarshall:
    def __init__(self):
        self.parents = {}
        self.paths = {}

    def find(self, graph):
        self.graph = graph
        self.init_parents()
        g = graph
        p = self.parents

        for k in g:
            for i in g:
                for j in g:
                    if g[i][k] + g[k][j] < g[i][j]:
                        g[i][j] = g[i][k] + g[k][j]
                        p[i][j] = k

        return self.restore_paths()

    def init_parents(self):
        for i in self.graph:
            parent_row = {}
            path_row = {}
            for j in self.graph:
                parent_row[j] = None
                path_row[j] = None
            self.parents[i] = parent_row
            self.paths[i] = path_row

    def restore_paths(self):
        q = deque()

        for i, row in enumerate(self.graph):
            for j, col in enumerate(self.graph):
                if math.isfinite(self.graph[row][col]):
                    self.paths[row][col] = deque()
                    mid = self.parents[row][col]
                    if mid:
                        self.paths[row][col].append(mid)
                        q.append((row, col, self.parents[row][mid], self.parents[mid][col]))
                    else:
                        q.append((row, col, None, None))

        while True:
            if not q:
                break

            node = q.popleft()
            row, col, left, right = node

            if left:
                self.paths[row][col].appendleft(left)
                q.append((row, col, self.parents[row][left], None))
            if right:
                self.paths[row][col].append(right)
                q.append((row, col, None, self.parents[col][right]))
            if not left and not right:
                self.paths[row][col].appendleft(row)
                self.paths[row][col].append(col)
