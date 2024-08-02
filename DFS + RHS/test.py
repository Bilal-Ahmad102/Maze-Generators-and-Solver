class RightHandSolver:
    def __init__(self, start, end, grid,rows, cols):
        self.current = start
        self.end = end
        self.grid = grid
        self.cols = cols
        self.rows = rows

        self.direction = 1   # 0: left, 1: top, 2: right, 3: bottom
        self.finished = False
        self.path = []

    def index(self, i, j):
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return None
        return i + j * self.rows
    
    def step(self):
        
        if self.current == self.end:
            self.finished = True
            print("Maze solved!")
            return None, None
        
        self.path.append(self.current)
        self.current.visited = True

        # Try to turn right from every direction current is facing
        right_dir = (self.direction + 1) % 4
        
        if not self.current.flags[right_dir]:
            self.direction = right_dir
            next_cell = self.move()
            if next_cell:
                self.current = next_cell
                return self.path[-1], self.current

        # Go straight if possible
        if not self.current.flags[self.direction]:
            next_cell = self.move()
            if next_cell:
                self.current = next_cell
                return self.path[-1], self.current

        # Turn left
        self.direction = (self.direction - 1) % 4
        return self.current, self.current
    
    def move(self):
        next_cell = None
        next_x, next_y = self.current.x, self.current.y

        if self.direction == 0:  # left
            next_x -= 1
        elif self.direction == 1:  # Up
            next_y += 1
        elif self.direction == 2:  # Right
            next_x += 1
        elif self.direction == 3:  # down
            next_y -= 1

        index = self.index(next_x, next_y)
        if index is not None:
            next_cell = self.grid[index]
        else:
            print(f"Cannot move to {next_x},{next_y} - out of bounds")

        return next_cell