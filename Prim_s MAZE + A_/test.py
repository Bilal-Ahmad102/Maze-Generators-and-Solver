import heapq

class AStar:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.open_set = []
        self.came_from = {}
        self.g_score = {cell: float('inf') for cell in grid}
        self.f_score = {cell: float('inf') for cell in grid}
        self.g_score[start] = 0
        self.f_score[start] = self.heuristic(start, end)
        heapq.heappush(self.open_set, (self.f_score[start], start.id, start))
        self.current = None
        self.path = []

    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_neighbors(self, cell):
        neighbors = []
        for i, flag in enumerate(cell.flags):
            if not flag:
                if i == 0 and cell.x > 0:  # Left
                    neighbors.append(self.grid[cell.index(cell.x - 1, cell.y)])
                elif i == 1 and cell.y < cell.rows - 1:  # Top
                    neighbors.append(self.grid[cell.index(cell.x, cell.y + 1)])
                elif i == 2 and cell.x < cell.cols - 1:  # Right
                    neighbors.append(self.grid[cell.index(cell.x + 1, cell.y)])
                elif i == 3 and cell.y > 0:  # Bottom
                    neighbors.append(self.grid[cell.index(cell.x, cell.y - 1)])
        return neighbors

    def step(self):
        if self.open_set:
            _, _, self.current = heapq.heappop(self.open_set)

            if self.current == self.end:
                self.reconstruct_path()
                return True

            for neighbor in self.get_neighbors(self.current):
                tentative_g_score = self.g_score[self.current] + 1

                if tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = self.current
                    self.g_score[neighbor] = tentative_g_score
                    self.f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.end)
                    if neighbor not in [item[2] for item in self.open_set]:
                        heapq.heappush(self.open_set, (self.f_score[neighbor], neighbor.id, neighbor))

        return False

    def reconstruct_path(self):
        self.path = []
        current = self.end
        while current in self.came_from:
            self.path.append(current)
            current = self.came_from[current]
        self.path.append(self.start)
        self.path.reverse()