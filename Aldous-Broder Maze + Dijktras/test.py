import heapq
from itertools import count

class Dijkstra:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.distances = {cell: float('inf') for cell in grid}
        self.distances[start] = 0
        self.previous = {cell: None for cell in grid}
        self.counter = count()
        self.heap = [(0, next(self.counter), start)]
        self.current = None
        self.path = []
        self.finished = False

    def step(self):
        if self.heap and not self.finished:
            current_distance, _, self.current = heapq.heappop(self.heap)

            if self.current == self.end:
                self.finished = True
                self.reconstruct_path()
                return

            for neighbor in self.current.checkNeighbours(self.grid):
                if self.are_connected(self.current, neighbor):
                    distance = current_distance + 1
                    if distance < self.distances[neighbor]:
                        self.distances[neighbor] = distance
                        self.previous[neighbor] = self.current
                        heapq.heappush(self.heap, (distance, next(self.counter), neighbor))

    def are_connected(self, cell1, cell2):
        if cell1.x == cell2.x:
            if cell1.y < cell2.y:
                return not cell1.flags[1] and not cell2.flags[3]
            else:
                return not cell1.flags[3] and not cell2.flags[1]
        elif cell1.y == cell2.y:
            if cell1.x < cell2.x:
                return not cell1.flags[2] and not cell2.flags[0]
            else:
                return not cell1.flags[0] and not cell2.flags[2]
        return False

    def reconstruct_path(self):
        current = self.end
        while current:
            self.path.append(current)
            current = self.previous[current]
        self.path.reverse()